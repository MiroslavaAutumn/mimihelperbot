from googletrans import Translator


def get_translation(user_text, src_lang, dest_lang):
    translator = Translator()
    translations = translator.translate([user_text], src=src_lang, dest=dest_lang)
    answers = []
    for translation in translations:
        answers.append('Перевод: ' + translation.text)
    return answers[0]


if __name__ == '__main__':
    user_text = input('введи текст ')
    result = get_translation(user_text)
    print(result)
