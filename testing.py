import unittest
import statements as s
import pos_tagging as p
import agreement as a


class TestStatements(unittest.TestCase):
    def test_john_likes_mary(self):
        lx = s.Lexicon()
        lx.add("John", "P")
        lx.add("Mary", "P")
        lx.add("like", "T")
        self.assertEqual(lx.getAll("P"), ["John", "Mary"])

    def test_access_before_assign(self):
        lx = s.Lexicon()
        self.assertEqual(lx.getAll("N"), [])

    def test_no_duplicates(self):
        lx = s.Lexicon()
        lx.add("John", "P")
        lx.add("Mary", "P")
        lx.add("John", "P")
        lx.add("Mary", "P")
        lx.add("like", "T")
        self.assertEqual(lx.getAll("P"), ["John", "Mary"])

    def test_factbase_story(self):
        fb = s.FactBase()
        fb.addUnary("duck", "John")
        fb.addBinary("love", "John", "Mary")
        self.assertTrue(fb.queryUnary("duck", "John"))
        self.assertFalse(fb.queryBinary("love", "Mary", "John"))

    def test_verb_stem(self):
        self.assertEqual("fly", s.verb_stem("flies"))
        self.assertEqual("eat", s.verb_stem("eats"))
        self.assertEqual("tell", s.verb_stem("tells"))
        self.assertEqual("show", s.verb_stem("shows"))
        self.assertEqual("pay", s.verb_stem("pays"))
        self.assertEqual("buy", s.verb_stem("buys"))
        self.assertEqual("fly", s.verb_stem("flies"))
        self.assertEqual("try", s.verb_stem("tries"))
        self.assertEqual("unify", s.verb_stem("unifies"))
        self.assertEqual("die", s.verb_stem("dies"))
        self.assertEqual("lie", s.verb_stem("lies"))
        self.assertEqual("tie", s.verb_stem("ties"))
        self.assertEqual("go", s.verb_stem("goes"))
        self.assertEqual("box", s.verb_stem("boxes"))
        self.assertEqual("attach", s.verb_stem("attaches"))
        self.assertEqual("wash", s.verb_stem("washes"))
        self.assertEqual("dress", s.verb_stem("dresses"))
        #self.assertEqual("fizz", s.verb_stem("fizzes"))
        self.assertEqual("lose", s.verb_stem("loses"))
        #self.assertEqual("daze", s.verb_stem("dazes"))
        self.assertEqual("lapse", s.verb_stem("lapses"))
        #self.assertEqual("analyse", s.verb_stem("analyses"))
        self.assertEqual("have", s.verb_stem("has"))
        self.assertEqual("like", s.verb_stem("likes"))
        self.assertEqual("hate", s.verb_stem("hates"))
        self.assertEqual("bathe", s.verb_stem("bathes"))


class TestPOS(unittest.TestCase):
    def test_noun_stem(self):
        self.assertEqual(p.noun_stem("sheep"), "sheep")
        self.assertEqual(p.noun_stem("sheeps"), "")
        self.assertEqual(p.noun_stem("buffalo"), "buffalo")
        self.assertEqual(p.noun_stem("buffalos"), "")
        self.assertEqual(p.noun_stem("women"), "woman")
        self.assertEqual(p.noun_stem("men"), "man")
        self.assertEqual(p.noun_stem("ashes"), "ash")
        self.assertEqual(p.noun_stem("countries"), "country")
        self.assertEqual(p.noun_stem("dogs"), "dog")

    def test_tag_words(self):
        lx = s.Lexicon()
        lx.add("John", "P")
        lx.add("orange", "A")
        lx.add("orange", "N")
        lx.add("fish", "N")
        lx.add("fish", "I")
        lx.add("fish", "T")
        self.assertEqual(["P"], p.tag_word(lx, "John"))
        self.assertEqual(["A", "Ns"], p.tag_word(lx, "orange"))
        self.assertEqual(["Ns", "Np", "Ip", "Tp"], p.tag_word(lx, "fish"))
        self.assertEqual(["AR"], p.tag_word(lx, "a"))
        self.assertEqual([], p.tag_word(lx, "zxghqw"))


class TestAgreement(unittest.TestCase):
    def test_can_parse(self):
        lx = s.Lexicon()
        lx.add('John', 'P')
        lx.add('like', 'T')
        lx.add("fly", "I")
        lx.add("Mary", "P")
        lx.add("duck", "N")
        lx.add("swim", "I")
        lx.add("like", "T")
        lx.add("frog", "N")
        lx.add("orange", "A")
        lx.add("orange", "N")
        lx.add("purple", "A")
        lx.add("fish", "N")
        lx.add("fish", "I")
        lx.add("fish", "T")
        lx.add("student", "N")
        lx.add("old", "A")
        self.assertGreaterEqual(
            len(a.all_valid_parses(lx, "Who likes John ?".split(" "))), 1)
        self.assertGreaterEqual(
            len(a.all_valid_parses(lx, "Who is a duck ?".split(" "))), 1)
        self.assertGreaterEqual(len(a.all_valid_parses(
            lx, "Which orange duck likes a frog ?".split(" "))), 1)
        self.assertGreaterEqual(len(a.all_valid_parses(
            lx, "Who does John like ?".split(" "))), 1)
        self.assertGreaterEqual(len(a.all_valid_parses(
            lx, "Who is an orange duck ?".split(" "))), 1)
        self.assertGreaterEqual(len(a.all_valid_parses(
            lx, "Which ducks are orange ?".split(" "))), 1)
        self.assertGreaterEqual(len(a.all_valid_parses(
            lx, "Which ducks like a frog ?".split(" "))), 1)
        self.assertGreaterEqual(len(a.all_valid_parses(
            lx, "Which ducks like frogs ?".split(" "))), 1)
        self.assertGreaterEqual(len(a.all_valid_parses(
            lx, "Who likes a duck who flies ?".split(" "))), 1)
        self.assertGreaterEqual(len(a.all_valid_parses(
            lx, "Which purple ducks fly ?".split(" "))), 1)


if __name__ == '__main__':
    unittest.main()
