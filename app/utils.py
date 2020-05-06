
#funkcja ekstrakcja składowych opinii
def extract_feature(opinion, selector, attribute = None):
    try:
        if not attribute:
            return opinion.select(selector).pop().get_text().strip()
        else:
            return opinion.select(selector).pop()[attribute]
    except IndexError:
        return None

def remove_whitespaces(text):
    try:
        for char in ["\n", "\r"]:
            text = text.replace(char, ". ")
        return text
    except AttributeError:
        pass