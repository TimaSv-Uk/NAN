import os
from pathlib import Path

from cryptall_2.visualize_encoding import (
    visualy_encode_image_file,
)

BASE_DIR = Path(__file__).parent.parent.parent.parent

if __name__ == "__main__":
    bite_ecncode_mod: int = 256
    d_mod: int = 128
    seed: int = 42

    image_dir = BASE_DIR / "tests/test_files/visual_encoded/input_img"
    base_save_dir = BASE_DIR / "tests/test_files/visual_encoded/encoded_img"
    # os.makedirs(base_save_dir, exist_ok=True)
    print(image_dir)
    for d_mod_i in range(32, d_mod + 1, 32):
        save_image_mod_dir = os.path.join(base_save_dir, f"d_mod_{d_mod_i}")
        os.makedirs(save_image_mod_dir, exist_ok=True)

        for name in os.listdir(image_dir):
            image_name = name
            image_file_path = os.path.join(image_dir, name)
            image_save_file_path = os.path.join(save_image_mod_dir, name)
            visualy_encode_image_file(
                image_file_path, image_save_file_path, bite_ecncode_mod, d_mod_i, seed
            )
            print(f"encoded {image_file_path} saved a{image_save_file_path}")
