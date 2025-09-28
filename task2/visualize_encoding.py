import numpy as np
from PIL import Image

from task2 import (
    encode_assignment5,
    change_first_symbol_based_on_random_vector,
)


def encode_image_file_without_header(
    file_path: str = "test_files/data2.txt",
    save_encoded_file_path: str = "test_files/data2_encoded.txt",
    seed: int = 42,
):
    """
    Saves encoded file that can be read and visualy encryption algirithm
    """

    img = Image.open(file_path)
    pixels = np.array(img)
    pixels_vector = pixels.flatten()

    pixels_vector = change_first_symbol_based_on_random_vector(pixels_vector, seed)
    encoded_pixels_vector = encode_assignment5(pixels_vector)

    encoded_pixels = encoded_pixels_vector.reshape(np.shape(pixels))
    Image.fromarray(encoded_pixels).save(save_file_path)


if __name__ == "__main__":
    image_name = "img.jpg"

    file_path = f"test_files/{image_name}"
    save_file_path = f"test_files/visual_encoded_{image_name}"
    encode_image_file_without_header(file_path, save_file_path, 42)
