import unittest

import parse_ljsl


TEST_CORPUS = '''There is some text followed by information about
@registers:TEST#(120:5:3) as well as a seperate mixed entry about:

@registers:OTHERTEST#(1:3),TEST#(1:5:3),OTHERTEST#(1:3)
'''

TEST_CORPUS_MANY_WITH_INVALID = '''There is some text followed by information
about @registers:TEST#(120:5:3) and a mistake in @registers:TEST#(120d:5:3) but
not in @registers:OTHERTEST#(120:5:3)'''

TEST_CORPUS_INVALID = '''There is an invalid entry %s before the valid entry
@registers:VALID#(1:2:3)'''

POSTFIX_CORPUS = '''Of course
@registers:VALID#(1:2:3)AFTERWARDS,VALID#(4:5:6),VALIDAGAIN#(101:2:3)AFTERWARDS
demonstrate that some registers have postfixes as well. On the other hand,
some like @registers:VALID#(100:200:300) do not.'''


class ExpandInjectDataFieldsTests(unittest.TestCase):

    def test_find_names(self):
        matches = parse_ljsl.find_names(TEST_CORPUS)

        self.assertEqual(len(matches), 2)

        lengths = map(lambda x: len(x), matches)
        self.assertEqual([1, 3], lengths)

        target_match = matches[0][0]
        self.assertEqual(target_match.prefix, 'TEST')
        self.assertEqual(target_match.start_num, 120)
        self.assertEqual(target_match.num_regs, 5)
        self.assertEqual(target_match.num_between_regs, 3)
        self.assertEqual(target_match.postfix, '')

        target_match = matches[1][0]
        self.assertEqual(target_match.prefix, 'OTHERTEST')
        self.assertEqual(target_match.start_num, 1)
        self.assertEqual(target_match.num_regs, 3)
        self.assertEqual(target_match.num_between_regs, None)
        self.assertEqual(target_match.postfix, '')

        target_match = matches[1][1]
        self.assertEqual(target_match.prefix, 'TEST')
        self.assertEqual(target_match.start_num, 1)
        self.assertEqual(target_match.num_regs, 5)
        self.assertEqual(target_match.num_between_regs, 3)
        self.assertEqual(target_match.postfix, '')

        target_match = matches[1][2]
        self.assertEqual(target_match.prefix, 'OTHERTEST')
        self.assertEqual(target_match.start_num, 1)
        self.assertEqual(target_match.num_regs, 3)
        self.assertEqual(target_match.num_between_regs, None)
        self.assertEqual(target_match.postfix, '')

    def test_find_name_after_invalid(self):
        matches = parse_ljsl.find_names(
            TEST_CORPUS_MANY_WITH_INVALID)

        self.assertEqual(len(matches), 2)
        target_match = matches[0][0]
        self.assertEqual(target_match.prefix, 'TEST')

        self.assertEqual(len(matches), 2)
        target_match = matches[1][0]
        self.assertEqual(target_match.prefix, 'OTHERTEST')

    def test_wrong_prefix(self):
        test_corpus = TEST_CORPUS_INVALID % '@results:INVALID#(0:1)'
        matches = parse_ljsl.find_names(test_corpus)

        self.assertEqual(len(matches), 1)
        target_match = matches[0][0]
        self.assertEqual(target_match.prefix, 'VALID')

    def test_missing_colon(self):
        test_corpus = TEST_CORPUS_INVALID % '@registersINVALID#(0:1)'
        matches = parse_ljsl.find_names(test_corpus)

        self.assertEqual(len(matches), 1)
        target_match = matches[0][0]
        self.assertEqual(target_match.prefix, 'VALID')

    def test_missing_pound(self):
        test_corpus = TEST_CORPUS_INVALID % '@registers:INVALID(0:1)'
        matches = parse_ljsl.find_names(test_corpus)

        self.assertEqual(len(matches), 1)
        target_match = matches[0][0]
        self.assertEqual(target_match.prefix, 'VALID')

    def test_missing_front_paren(self):
        test_corpus = TEST_CORPUS_INVALID % '@registers:INVALID#0:1)'
        matches = parse_ljsl.find_names(test_corpus)

        self.assertEqual(len(matches), 1)
        target_match = matches[0][0]
        self.assertEqual(target_match.prefix, 'VALID')

    def test_missing_back_paren(self):
        test_corpus = TEST_CORPUS_INVALID % '@registers:INVALID#(0:1'
        matches = parse_ljsl.find_names(test_corpus)

        self.assertEqual(len(matches), 1)
        target_match = matches[0][0]
        self.assertEqual(target_match.prefix, 'VALID')

    def test_missing_param(self):
        test_corpus = TEST_CORPUS_INVALID % '@registers:INVALID#(0)'
        matches = parse_ljsl.find_names(test_corpus)

        self.assertEqual(len(matches), 1)
        target_match = matches[0][0]
        self.assertEqual(target_match.prefix, 'VALID')

    def test_missing_param_value(self):
        test_corpus = TEST_CORPUS_INVALID % '@registers:INVALID#(0:)'
        matches = parse_ljsl.find_names(test_corpus)

        self.assertEqual(len(matches), 1)
        target_match = matches[0][0]
        self.assertEqual(target_match.prefix, 'VALID')

    def test_missing_optional_param_value(self):
        test_corpus = TEST_CORPUS_INVALID % '@registers:INVALID#(0:1:)'
        matches = parse_ljsl.find_names(test_corpus)

        self.assertEqual(len(matches), 1)
        target_match = matches[0][0]
        self.assertEqual(target_match.prefix, 'VALID')

    def test_postfix_values(self):
        matches = parse_ljsl.find_names(POSTFIX_CORPUS)

        self.assertEqual(len(matches), 2)
        self.assertEqual(len(matches[0]), 3)
        self.assertEqual(len(matches[1]), 1)
        
        target_match = matches[0][0]
        self.assertEqual(target_match.prefix, 'VALID')
        self.assertEqual(target_match.start_num, 1)
        self.assertEqual(target_match.num_regs, 2)
        self.assertEqual(target_match.num_between_regs, 3)
        self.assertEqual(target_match.postfix, 'AFTERWARDS')

        target_match = matches[0][1]
        self.assertEqual(target_match.prefix, 'VALID')
        self.assertEqual(target_match.start_num, 4)
        self.assertEqual(target_match.num_regs, 5)
        self.assertEqual(target_match.num_between_regs, 6)
        self.assertEqual(target_match.postfix, '')

        target_match = matches[0][2]
        self.assertEqual(target_match.prefix, 'VALIDAGAIN')
        self.assertEqual(target_match.start_num, 101)
        self.assertEqual(target_match.num_regs, 2)
        self.assertEqual(target_match.num_between_regs, 3)
        self.assertEqual(target_match.postfix, 'AFTERWARDS')

        target_match = matches[1][0]
        self.assertEqual(target_match.prefix, 'VALID')
        self.assertEqual(target_match.start_num, 100)
        self.assertEqual(target_match.num_regs, 200)
        self.assertEqual(target_match.num_between_regs, 300)
        self.assertEqual(target_match.postfix, '')


if __name__ == '__main__':
    unittest.main()
