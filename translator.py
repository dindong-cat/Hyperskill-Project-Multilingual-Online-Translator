import requests
import argparse
from bs4 import BeautifulSoup


def check_connection(original_language, language, word):
    url = f"https://context.reverso.net/translation/{original_language}-{language}/{word}"
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if r:
        return [f"{r.status_code} OK", r]
    return False


def better_translation_format(language, translation_target, word):
    if not translation_target:
        print(f"Sorry, unable to find {word}")
        exit()

    print(f"{language.title()} Translations:")
    print((translation_target[0]))
    print()
    with open(f"{word}.txt", "a", encoding="utf-8") as f:
        f.writelines(f"{language.title()} Translations:\n")
        f.writelines(translation_target[0])
        f.writelines("\n\n")


def better_example_format(language, example_target, example_target_translated, word):
    if not example_target:
        print(f"Sorry, unable to find {word}")
        exit()

    print(f"{language.title()} Example:")
    print(example_target[0])
    print(example_target_translated[0])
    print()
    with open(f"{word}.txt", "a", encoding="utf-8") as f:
        f.writelines(f"{language.title()} Example:\n")
        f.writelines(example_target[0] + "\n")
        f.writelines(example_target_translated[0] + "\n")
        f.writelines("\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("original_language")
    parser.add_argument("language", default="all")
    parser.add_argument("word")
    args = parser.parse_args()
    language_list = ["Arabic", "German", "English", "Spanish", "French",
                     "Hebrew", "Japanese", "Dutch", "Polish", "Portuguese",
                     "Romanian", "Russian", "Turkish"]
    original_language = args.original_language
    language = args.language
    word = args.word
    print()

    if language != "all" and language not in language_list:
        print(f"Sorry, the program doesn't support {language}")
        exit()

    if language != "all":
        target_language_list = [language]
    else:
        target_language_list = [i for i in language_list if i != original_language.title()]

    with requests.Session() as s:
        s.get("https://context.reverso.net/translation")

        for i in target_language_list:
            language = i.lower()
            url = f"https://context.reverso.net/translation/{original_language}-{language}/{word}"
            r = s.get(url, headers={'User-Agent': 'Mozilla/5.0'})

            soup = BeautifulSoup(r.content, "html.parser")
            translation_target = soup.find_all("a", {"class": "translation"})
            translation_target = [i.text.strip() for i in translation_target if i.text.strip() != "Translation"]
            example_target = soup.find_all("div", {"class": "src"})
            example_target = [i.text.strip() for i in example_target if i.text.strip() != ""]
            example_target_translated = soup.find_all("div", {"class": "trg"})
            example_target_translated = [i.text.strip() for i in example_target_translated if i.text.strip() != ""]
            better_translation_format(language, translation_target, word)
            better_example_format(language, example_target, example_target_translated, word)


if __name__ == "__main__":
    main()
