from cryptall_2.encode_decode import save_file_digests


if __name__ == "__main__":
    number_of_digests = 4

    file_path = "tests/test_results/encoded/img_encoded.jpg"
    save_file_path = "tests/digests/img_encoded/"

    save_file_digests(number_of_digests, file_path, save_file_path)

    print(f"{number_of_digests} digests of {file_path}; Saved at {save_file_path}")
