def sanitize_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\u2018', "'").replace('\u2019', "'")
    text = text.replace('\u2014', '-').replace('\u2013', '-')
    return text.encode('ascii', 'ignore').decode('ascii')