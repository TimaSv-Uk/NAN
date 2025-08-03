from task2 import get_encoded_text_int


def text_sameness_percentage(text1: str, text2: str) -> float:
    if len(text1) != len(text2) or len(text1) == 0:
        return 0.0
    same_symbols = sum(1 for a, b in zip(text1, text2) if a == b)
    return same_symbols / len(text1)


if __name__ == "__main__":
    print(text_sameness_percentage("bon", "bob"))
