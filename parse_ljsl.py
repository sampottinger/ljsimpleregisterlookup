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
DIGITS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
VALID_NAME_CHAR_REGEX = re.compile('[A-Z]|[0-9]|_')

TagComponent = collections.namedtuple(
    'TagComponent',
    [
        'prefix',
        'start_num',
        'num_regs',
        'num_between_regs',
        'postfix',
        'includes_ljmmm'
    ]
)


class ParserAutomaton:

    def __init__(self, start_state=STATE_LOOKING_FOR_AT):
        self.state = start_state
        self.tags = []
        self.errors = []
        self.rules = {
            STATE_LOOKING_FOR_AT: self.character_match(
                '@',
                STATE_LOOKING_FOR_R1,
                STATE_LOOKING_FOR_AT
            ),
            STATE_LOOKING_FOR_R1: self.character_match(
                'r',
                STATE_LOOKING_FOR_E1,
                STATE_LOOKING_FOR_AT
            ),
            STATE_LOOKING_FOR_E1: self.character_match(
                'e',
                STATE_LOOKING_FOR_G,
                STATE_LOOKING_FOR_AT
            ),
            STATE_LOOKING_FOR_G: self.character_match(
                'g',
                STATE_LOOKING_FOR_I,
                STATE_LOOKING_FOR_AT
            ),
            STATE_LOOKING_FOR_I: self.character_match(
                'i',
                STATE_LOOKING_FOR_S1,
                STATE_LOOKING_FOR_AT
            ),
            STATE_LOOKING_FOR_S1: self.character_match(
                's',
                STATE_LOOKING_FOR_T,
                STATE_LOOKING_FOR_AT
            ),
            STATE_LOOKING_FOR_T: self.character_match(
                't',
                STATE_LOOKING_FOR_E2,
                STATE_LOOKING_FOR_AT
            ),
            STATE_LOOKING_FOR_E2: self.character_match(
                'e',
                STATE_LOOKING_FOR_R2,
                STATE_LOOKING_FOR_AT
            ),
            STATE_LOOKING_FOR_R2: self.character_match(
                'r',
                STATE_LOOKING_FOR_S2,
                STATE_LOOKING_FOR_AT
            ),
            STATE_LOOKING_FOR_S2: self.character_match(
                's',
                STATE_LOOKING_FOR_COLON,
                STATE_LOOKING_FOR_AT
            ),
            STATE_LOOKING_FOR_COLON: self.looking_for_colon,
            STATE_READING_PREFIX: self.reading_prefix,
            STATE_LOOKING_FOR_OPEN_PAREN: self.character_match(
                '(',
                STATE_READING_PARAM_1,
                STATE_LOOKING_FOR_AT
            ),
            STATE_READING_PARAM_1: self.reading_param_1,
            STATE_READING_PARAM_2: self.reading_param_2,
            STATE_READING_PARAM_3: self.reading_param_3,
            STATE_READING_POSTFIX: self.reading_postfix
        }

    def next_character(self, char):
        self.rules[self.state](char)

    def character_match(self, target_char, next_state, fail_state):
        def inner(char):
            if char == target_char: self.state = next_state
            else: self.state = fail_state
        return inner

    def looking_for_colon(self, char):
        if char == ':':
            self.state = STATE_READING_PREFIX
            self.clear_current_subtag()
            self.tag_components = []
        else: self.state = STATE_LOOKING_FOR_AT

    def reading_prefix(self, char):
        if char == '#':
            self.state = STATE_LOOKING_FOR_OPEN_PAREN
            self.param_1 = ''
        elif char != None and VALID_NAME_CHAR_REGEX.match(char):
            self.prefix += char
        else:
            self.reading_postfix(char)

    def reading_param_1(self, char):
        if char == ':' and len(self.param_1) > 0:
            self.state = STATE_READING_PARAM_2
            self.param_2 = ''
        elif char not in DIGITS:
            self.state = STATE_LOOKING_FOR_AT
        else: self.param_1 += char

    def reading_param_2(self, char):
        if char == ':' and len(self.param_2) > 0:
            self.state = STATE_READING_PARAM_3
            self.param_3 = ''
        elif char == ')' and len(self.param_2) > 0:
            self.state = STATE_READING_POSTFIX
        elif char not in DIGITS:
            self.state = STATE_LOOKING_FOR_AT
        else: self.param_2 += char

    def reading_param_3(self, char):
        if char == ')' and len(self.param_3) > 0:
            self.state = STATE_READING_POSTFIX
        elif char not in DIGITS:
            self.state = STATE_LOOKING_FOR_AT
        else: self.param_3 += char

    def reading_postfix(self, char):
        if char == ',':
            self.state = STATE_READING_PREFIX
            self.try_to_accept_current_component()
            self.clear_current_subtag()
        elif char != None and VALID_NAME_CHAR_REGEX.match(char):
            self.postfix += char
        else:
            self.state = STATE_LOOKING_FOR_AT
            self.try_to_accept_current_component()
            self.end_tag()

    def try_to_accept_current_component(self):
        if self.param_1 == None:
            self.tag_components.append(
                TagComponent(
                    self.prefix,
                    None,
                    None,
                    None,
                    None,
                    False
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
                err = '%s:%s:%s must all be integers.' % params_set
                self.errors.append(err)
                return

            self.tag_components.append(
                TagComponent(
                    self.prefix,
                    param_1,
                    param_2,
                    param_3,
                    self.postfix,
                    True
                )
            )

    def clear_current_subtag(self):
        self.prefix = ''
        self.postfix = ''
        self.param_1 = None
        self.param_2 = None
        self.param_3 = None

    def end_tag(self):
        self.tags.append(self.tag_components)


def find_names(msg):
    parser = ParserAutomaton()
    for char in msg:
        parser.next_character(char)
    parser.next_character(None)
    return parser.tags
