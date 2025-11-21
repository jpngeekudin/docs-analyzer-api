def text_split(text: str, n: int):
    result = []
    for i in range(0, len(text), n):
        result.append(text[i:i+n])
    return result