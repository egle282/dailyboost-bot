import unittest
from languages import t, LANGUAGES

class TestLanguages(unittest.TestCase):
    def test_required_keys_across_all_languages(self):
        base_keys = set(LANGUAGES["ru"].keys())
        for lang_code in ["en", "es"]:
            lang_keys = set(LANGUAGES[lang_code].keys())
            missing = base_keys - lang_keys
            self.assertEqual(len(missing), 0, f"Language {lang_code} is missing keys: {missing}")

    def test_translation_formatting(self):
        res = t("ru", "start", name="Дмитрий")
        self.assertIn("Дмитрий", res)
        self.assertIn("DailyBoost", res)

    def test_fallback_language(self):
        res = t("non_existing_lang", "start", name="John")
        self.assertIn("John", res)

if __name__ == "__main__":
    unittest.main()
