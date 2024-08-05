import re


class Normalizer:
    def __init__(self, verbs_path):
        self.mi_patterns = r"\bن?می[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]+"

        self.punc_after = r"\.:!،؛؟»\]\)\}"
        self.punc_before = r"«\[\(\{"
        self.all_punc_marks = r"[\.:!،؛؟»\'\]\)\}|«\[\(\/\{><+\-?!=_]"

        self.number_not_persian = "0123456789%٠١٢٣٤٥٦٧٨٩"
        self.number_persian = "۰۱۲۳۴۵۶۷۸۹٪۰۱۲۳۴۵۶۷۸۹"

        self.arabic_patterns = [
            (r"[\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652]", ""),
            (r"[ك]", "ک"),
            (r"[ي]", "ی"),
            (r"[هٔ]", "ه"),
            (r"[أ]", "ا"),
        ]

        self.punctuation_spacing_patterns = [
            (r'" ([^\n"]+) "', r'"\1"'),
            (r" ([" + self.punc_after + "])", r"\1"),
            (r"([" + self.punc_before + "]) ", r"\1"),
            (r"([" + self.punc_after[:3] + "])([^ " + self.punc_after + r"\d۰۱۲۳۴۵۶۷۸۹])", r"\1 \2"),
            (r"([" + self.punc_after[3:] + "])([^ " + self.punc_after + "])", r"\1 \2"),
            (r"([^ " + self.punc_before + "])([" + self.punc_before + "])", r"\1 \2"),
            (r"(\d)([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])", r"\1 \2"),
            (r"([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])(\d)", r"\1 \2"),
        ]

        self.unicode_replacements = [
            ("﷽", " بسم الله الرحمن الرحیم "),
            (" ﷼", " ریال"),
            ("(ﷰ|ﷹ)", " صلی "),
            (" ﷲ", " الله"),
            (" ﷳ", " اکبر"),
            (" ﷴ", " محمد"),
            (" ﷵ", " صلعم"),
            (" ﷶ", " رسول"),
            (" ﷷ", " علیه"),
            (" ﷸ", " وسلم"),
            (r"ﻵ|ﻶ|ﻷ|ﻸ|ﻹ|ﻺ|ﻻ|ﻼ", " لا"),
        ]

        self.extra_space_patterns = [
            (r" {2,}", " "),
            (r"\n{3,}", "\n\n"),
            (r"\u200c{2,}", "\u200c"),
            (r"\u200c{1,} ", " "),
            (r" \u200c{1,}", " "),
            (r"\b\u200c*\B", " "),
            (r"\B\u200c*\b", " "),
            (r"[ـ\r]", " "),
        ]

        self.spacing_patterns = [
            (r"\xa0", " "),
            (r"([^ ]) ی ", r"\1‌ی "),
            (r"(^| )(ن?می) ", r"\1\2‌"),
            (
            r"(?<=[^\n\d" + self.punc_after + self.punc_before + r"]{2}) (تر(ین?)?|گری?|های?)(?=[ \n" + self.punc_after + self.punc_before + r"]|$)",
            r"‌\1"),
            (r"([^ ]ه) (ا(م|یم|ش|ند|ی|ید|ت))(?=[ \n" + self.punc_after + r"]|$)", r"\1‌\2"),
            (r"(ه)(ها)", r"\1‌\2"),
        ]

        with open(verbs_path, encoding="utf8") as verbs_file:
            verbs = [verb.strip() for verb in verbs_file if verb]
            self.present_bons = {verb[1:].split("#")[0].strip() for verb in verbs[1:]}
            self.past_bons = {verb.split("#")[1] for verb in verbs}

    @staticmethod
    def regex_replace(patterns, text):
        for pattern, repl in patterns:
            text = re.sub(pattern, repl, text)
        return text

    def spacing_correction(self, text):
        text = self.regex_replace(self.extra_space_patterns, text)
        text = self.regex_replace(self.punctuation_spacing_patterns, text)
        text = self.regex_replace(self.spacing_patterns, text)
        return text

    def unicode_replacement(self, text):
        for old, new in self.unicode_replacements:
            text = re.sub(old, new, text)
        return text

    def persian_number(self, text):
        translation_table = str.maketrans(self.number_not_persian, self.number_persian)
        return text.translate(translation_table)

    def remove_special_chars(self, text):
        text = self.remove_punc_marks(text)
        text = self.remove_arabic_chars(text)
        return text

    def remove_arabic_chars(self, text):
        return self.regex_replace(self.arabic_patterns, text)

    def remove_punc_marks(self, text):
        return re.sub(self.all_punc_marks, "", text)

    def separate_mi(self, text):
        matches = re.findall(self.mi_patterns, text)
        for match in matches:
            replacement = re.sub(r"^(ن?می)", r"\1‌", match)
            verb_root = re.sub(r"^(ن?می)", "", match)
            for verb in self.present_bons.union(self.past_bons):
                if verb in verb_root:
                    text = text.replace(match, replacement)
        return text

    def normalize(self, text):
        text = self.remove_special_chars(text)
        text = self.separate_mi(text)
        text = self.persian_number(text)
        text = self.unicode_replacement(text)
        text = self.spacing_correction(text)
        return text
