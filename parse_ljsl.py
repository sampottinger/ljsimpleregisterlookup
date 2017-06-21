"""Logic to parse LabJack Scribe Language.

@author: Sam Pottinger (samnsparky, http://gleap.org)
@license: GNU GPL v2
"""

import collections
import re

STATE_LOOKING_FOR_AT = 1
STATE_LOOKING_FOR_R1 = 2
STATE_LOOKING_FOR_E1 = 3
STATE_LOOKING_FOR_G = 4
STATE_LOOKING_FOR_I = 5
STATE_LOOKING_FOR_S1 = 6
STATE_LOOKING_FOR_T = 7
STATE_LOOKING_FOR_E2 = 8
STATE_LOOKING_FOR_R2 = 9
STATE_LOOKING_FOR_S2 = 10
STATE_LOOKING_FOR_COLON = 11
STATE_LOOKING_FOR_HASH = 12
STATE_LOOKING_FOR_OPEN_PAREN = 13
STATE_READING_PREFIX = 14
STATE_READING_PARAM_1 = 15
STATE_READING_PARAM_2 = 16
STATE_READING_PARAM_3 = 17
STATE_READING_POSTFIX = 18
STATE_READING_TITLE = 19
STATE_RESET = 20
STATE_READING_DEVICE_TYPE = 21
DIGITS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
VALID_NAME_CHAR_REGEX = re.compile("[a-zA-Z]|[0-9]|_")
VALID_DEVICE_TYPE_CHAR_REGEX = VALID_NAME_CHAR_REGEX

TagComponent = collections.namedtuple(
    "TagComponent",
    [
        "title",
        "prefix",
        "start_num",
        "num_regs",
        "num_between_regs",
        "postfix",
        "includes_ljmmm",
        "device_types",
    ]
)


class ParserAutomaton:
    """Automaton to parse LJSL.

    An Automaton that scans for LJSL tags, converting each tag into a collection
    of TagComponents.
    """

    def __init__(self, start_state=STATE_LOOKING_FOR_AT):
        """Create a new ParserAutomaton in the state of looking for at.

        Create a new ParserAutomaton without any tags that starts in the state
        STATE_LOOKING_FOR_AT in which it is looking for the @ symbol.
        """
        self.state = start_state
        self.tags = []
        self.errors = []
        self.title = ""
        self.device_types = []
        self.device_type = ""
        self.rules = {
            STATE_LOOKING_FOR_AT: self.character_match(
                "@",
                STATE_LOOKING_FOR_R1,
                STATE_RESET
            ),
            STATE_LOOKING_FOR_R1: self.character_match(
                "r",
                STATE_LOOKING_FOR_E1,
                STATE_RESET
            ),
            STATE_LOOKING_FOR_E1: self.character_match(
                "e",
                STATE_LOOKING_FOR_G,
                STATE_RESET
            ),
            STATE_LOOKING_FOR_G: self.character_match(
                "g",
                STATE_LOOKING_FOR_I,
                STATE_RESET
            ),
            STATE_LOOKING_FOR_I: self.character_match(
                "i",
                STATE_LOOKING_FOR_S1,
                STATE_RESET
            ),
            STATE_LOOKING_FOR_S1: self.character_match(
                "s",
                STATE_LOOKING_FOR_T,
                STATE_RESET
            ),
            STATE_LOOKING_FOR_T: self.character_match(
                "t",
                STATE_LOOKING_FOR_E2,
                STATE_RESET
            ),
            STATE_LOOKING_FOR_E2: self.character_match(
                "e",
                STATE_LOOKING_FOR_R2,
                STATE_RESET
            ),
            STATE_LOOKING_FOR_R2: self.character_match(
                "r",
                STATE_LOOKING_FOR_S2,
                STATE_RESET
            ),
            STATE_LOOKING_FOR_S2: self.character_match(
                "s",
                STATE_LOOKING_FOR_COLON,
                STATE_RESET
            ),
            STATE_LOOKING_FOR_COLON: self.looking_for_colon,
            STATE_READING_TITLE: self.reading_title,
            STATE_READING_DEVICE_TYPE: self.reading_device_type,
            STATE_READING_PREFIX: self.reading_prefix,
            STATE_LOOKING_FOR_OPEN_PAREN: self.character_match(
                "(",
                STATE_READING_PARAM_1,
                STATE_RESET
            ),
            STATE_READING_PARAM_1: self.reading_param_1,
            STATE_READING_PARAM_2: self.reading_param_2,
            STATE_READING_PARAM_3: self.reading_param_3,
            STATE_READING_POSTFIX: self.reading_postfix,
            STATE_RESET: self.reset
        }

    def next_character(self, char):
        """Have the automaton parse the next character in the input language.

        @param char: The character to parse. Should be a string containing a
            single character.
        @type char: str
        """
        self.rules[self.state](char)

    def character_match(self, target_char, next_state, fail_state):
        """Create a character matching enclosure that changes automaton state.

        Function generator that returns a function that checks to see if the
        provided character is as expected. If it is, it changes this automaton's
        state to next_state and, if not, it changes the automaton's state to
        fail_state. This is largely used to check for @,r,e,g,i,s,t,e,r,s in
        succession.

        @param target_char: The character to look for.
        @type target_char: str
        @param next_state: The ID of the state to put this automaton in if the
            character is matched.
        @type next_state: int
        @param fail_state: The ID fo the state to put his automaton in if the
            character is not matched.
        @type fail_state: int
        @return: Function that checks a character (single character string) and
            changes state based on if that character was expected.
        @rtype: function
        """
        def inner(char):
            """Function that checks to see if the given char is expected.

            @param char: The character to check. Should be a single character
                string.
            @type char: str
            """
            if char == target_char: self.state = next_state
            else: self.state = fail_state

        return inner

    def reading_title(self, char):
        if char == ")": self.state = STATE_LOOKING_FOR_COLON
        else: self.title += char

    def reading_device_type(self, char):
        if char == "]":
            self.state = STATE_LOOKING_FOR_COLON
            self.accept_current_device_type()
        elif char == ",":
            self.accept_current_device_type()
        elif char != None and VALID_DEVICE_TYPE_CHAR_REGEX.match(char):
            self.device_type += char
        else:
            self.state = STATE_RESET
            self.accept_current_device_type()

    def looking_for_colon(self, char):
        if char == ":":
            self.state = STATE_READING_PREFIX
            self.clear_current_subtag()
            self.tag_components = []
        elif char == "(":
            self.state = STATE_READING_TITLE
        elif char == "[":
            self.state = STATE_READING_DEVICE_TYPE
        else: self.state = STATE_RESET

    def reading_prefix(self, char):
        if char == "#":
            self.state = STATE_LOOKING_FOR_OPEN_PAREN
            self.param_1 = ""
        elif char != None and VALID_NAME_CHAR_REGEX.match(char):
            self.prefix += char
        else:
            self.reading_postfix(char)

    def reading_param_1(self, char):
        if char == ":" and len(self.param_1) > 0:
            self.state = STATE_READING_PARAM_2
            self.param_2 = ""
        elif char not in DIGITS:
            self.state = STATE_RESET
        else: self.param_1 += char

    def reading_param_2(self, char):
        if char == ":" and len(self.param_2) > 0:
            self.state = STATE_READING_PARAM_3
            self.param_3 = ""
        elif char == ")" and len(self.param_2) > 0:
            self.state = STATE_READING_POSTFIX
        elif char not in DIGITS:
            self.state = STATE_RESET
        else: self.param_2 += char

    def reading_param_3(self, char):
        if char == ")" and len(self.param_3) > 0:
            self.state = STATE_READING_POSTFIX
        elif char not in DIGITS:
            self.state = STATE_RESET
        else: self.param_3 += char

    def reading_postfix(self, char):
        if char == ",":
            self.state = STATE_READING_PREFIX
            self.try_to_accept_current_component()
            self.clear_current_subtag()
        elif char != None and VALID_NAME_CHAR_REGEX.match(char):
            self.postfix += char
        else:
            self.state = STATE_RESET
            self.try_to_accept_current_component()
            self.end_tag()

    def accept_current_device_type(self):
        if not self.device_type.upper() in self.device_types:
            self.device_types.append(self.device_type.upper())
        self.device_type = ""

    def try_to_accept_current_component(self):
        if self.param_1 == None:
            self.tag_components.append(
                TagComponent(
                    self.title,
                    self.prefix,
                    None,
                    None,
                    None,
                    None,
                    False,
                    self.device_types,
                )
            )
        else:
            try:
                param_1 = int(self.param_1)
                param_2 = int(self.param_2)
                param_3 = self.param_3
                if param_3 != None: param_3 = int(self.param_3)
            except ValueError:
                params_set = (self.param_1, self.param_2, self.param_3)
                err = "%s:%s:%s must all be integers." % params_set
                self.errors.append(err)
                return

            self.tag_components.append(
                TagComponent(
                    self.title,
                    self.prefix,
                    param_1,
                    param_2,
                    param_3,
                    self.postfix,
                    True,
                    self.device_types,
                )
            )

    def clear_current_subtag(self):
        self.prefix = ""
        self.postfix = ""
        self.param_1 = None
        self.param_2 = None
        self.param_3 = None

    def end_tag(self):
        self.title = ""
        self.tags.append(self.tag_components)

    def reset(self, char):
        self.title = ""
        self.device_types = []
        if char == "@": self.state=STATE_LOOKING_FOR_R1


def find_names(msg):
    parser = ParserAutomaton()
    for char in msg:
        parser.next_character(char)
    parser.next_character(None)
    return parser.tags
