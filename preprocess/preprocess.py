import re
import parsivar
from string import punctuation
from collections import Counter
from pathlib import Path

import tqdm


class Preprocessor:
    top_k = {}
    pattern = re.compile(r'([؟!?]+|[\d.:]+|[:.،؛»\])}"«\[({/\\])')
    after_verbs = {
        "ام",
        "ای",
        "است",
        "ایم",
        "اید",
        "اند",
        "بودم",
        "بودی",
        "بود",
        "بودیم",
        "بودید",
        "بودند",
        "باشم",
        "باشی",
        "باشد",
        "باشیم",
        "باشید",
        "باشند",
        "شده",
        "نشده",
        "شوم",
        "شوی",
        "شود",
        "شویم",
        "شوید",
        "شوند",
        "شدم",
        "شدی",
        "شد",
        "شدیم",
        "شدید",
        "شدند",
        "نشوم",
        "نشوی",
        "نشود",
        "نشویم",
        "نشوید",
        "نشوند",
        "نشدم",
        "نشدی",
        "نشد",
        "نشدیم",
        "نشدید",
        "نشدند",
        "می‌شوم",
        "می‌شوی",
        "می‌شود",
        "می‌شویم",
        "می‌شوید",
        "می‌شوند",
        "می‌شدم",
        "می‌شدی",
        "می‌شد",
        "می‌شدیم",
        "می‌شدید",
        "می‌شدند",
        "نمی‌شوم",
        "نمی‌شوی",
        "نمی‌شود",
        "نمی‌شویم",
        "نمی‌شوید",
        "نمی‌شوند",
        "نمی‌شدم",
        "نمی‌شدی",
        "نمی‌شد",
        "نمی‌شدیم",
        "نمی‌شدید",
        "نمی‌شدند",

    }

    before_verbs = {
        "خواهم",
        "خواهی",
        "خواهد",
        "خواهیم",
        "خواهید",
        "خواهند",
        "نخواهم",
        "نخواهی",
        "نخواهد",
        "نخواهیم",
        "نخواهید",
        "نخواهند",
    }
    verbs = {}

    def __init__(self, normalizer, k, verbs_path):
        with Path(verbs_path).open(encoding="utf8") as verbs_file:
            verbs = list(
                reversed([verb.strip() for verb in verbs_file if verb]),
            )
            Preprocessor.verbs = {(verb.split("#")[0] + 'ه') for verb in verbs}
        self.normalizer = normalizer
        self.k = k

    @staticmethod
    def tokenization(text):
        text = Preprocessor.pattern.sub(r" \1 ", text.replace("\n", " ").replace("\t", " "))
        tokens = [word for word in text.split(" ") if word]
        tokens_cleaned = [token.strip('\xa0') for token in tokens if len(token.strip()) != 0]

        result = [""]
        for token in reversed(tokens_cleaned):
            if token in Preprocessor.before_verbs or (
                    result[-1] in Preprocessor.after_verbs and token in Preprocessor.verbs
            ):
                result[-1] = token + "_" + result[-1]
            else:
                result.append(token)
        return list(reversed(result[1:]))

    def normalize(self, text):
        return self.normalizer.normalize(text)

    @staticmethod
    def get_top_k_frequent(tokens, k):
        token_counts = Counter(tokens)
        sorted_tokens = sorted(token_counts.items(), key=lambda x: x[1], reverse=True)
        report = {token: count for token, count in sorted_tokens[:k]}
        return report

    def print_top_k(self):
        for token, count in self.top_k.items():
            print(f"Token: {token}, Count: {count}")

    @staticmethod
    def stem(tokens):
        stemmed = []
        stemmer = parsivar.FindStems()
        for token in tokens:
            stemmed.append(stemmer.convert_to_stem(token))
        return stemmed

    @staticmethod
    def remove_punctuations(text):
        return re.sub(f'[{punctuation}؟،٪×÷»«]+', '', text)

    def query_preprocess(self, content):
        punctuated_content = self.remove_punctuations(content)
        normalized_content = self.normalize(punctuated_content)
        tokens_of_a_sentence = self.tokenization(normalized_content)
        final_tokens_of_a_sentence = self.stem(tokens_of_a_sentence)
        tokens = [token for token in final_tokens_of_a_sentence if token not in self.top_k]
        return tokens

    def tokenize(self, text):
        return self.tokenization(text)

    def preprocess(self, docs):
        tokens = []
        counter = 0
        for idx in tqdm.tqdm(docs.keys()):
            content = docs[str(idx)]['content']
            punctuated_content = self.remove_punctuations(content)
            normalized_content = self.normalize(punctuated_content)
            all_tokens = self.tokenization(normalized_content)
            stemmed_tokens = self.stem(all_tokens)
            docs[str(idx)]['content'] = stemmed_tokens
            tokens += stemmed_tokens
            counter += 1
        self.top_k = self.get_top_k_frequent(tokens, self.k)
        for doc_id, doc_content in docs.items():
            docs[doc_id]['content'] = [token for token in doc_content['content']]
            # if doc_id == "12202":
            #     print([token for token in doc_content['content'] if token in self.top_k])
        return docs
