def text_sameness_percentage(text1: str, text2: str) -> float:
    if len(text1) != len(text2) or len(text1) == 0:
        return 0.0
    same_symbols = sum(1 for a, b in zip(text1, text2) if a == b)
    return same_symbols / len(text1)


def bites_sameness_percentage(bites1: [int], bites2: [int]) -> float:
    if len(bites1) != len(bites2) or len(bites1) == 0:
        return 0.0
    same_symbols = sum(1 for a, b in zip(bites1, bites2) if a == b)
    return same_symbols / len(bites1)


if __name__ == "__main__":
    print(text_sameness_percentage("bon", "bob"))
    print(bites_sameness_percentage([1, 2, 3], [1, 2, 9]))
