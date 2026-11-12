DIACRITICS = str.maketrans("ăâîșşțţ", "aaisstt")


def normalize(text: str) -> str:
    return text.lower().translate(DIACRITICS)
