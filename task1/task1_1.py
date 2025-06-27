def main():
    #  read file
    f = open("data1_1.txt", "r")

    text = f.read()

    chars = [ord(t) for t in text]

    f.close()

    # encode text and wrrite to file
    f = open("solution_task1_1.txt", "w")

    str_ascii_code_chars = [str(element) for element in chars]

    f.write(",".join(str_ascii_code_chars))

    f.close()

    # read vector from file and decode
    f = open("solution_task1_1.txt", "r")

    text = f.read().split(",")

    decoded_text = [chr(int(element)) for element in text]
    print("".join(decoded_text))

    f.close()


main()
