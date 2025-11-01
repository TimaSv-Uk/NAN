import os

from cryptall_2.visualize_encoding import (
    visualy_encode_video_file,
)

if __name__ == "__main__":
    bite_ecncode_mod: int = 256
    d_mod: int = 128
    seed: int = 42

    input_dir = "tests/test_files/visual_encoded/input_vid"
    base_save_dir = "tests/test_files/visual_encoded/encoded_vid"
    os.makedirs(base_save_dir, exist_ok=True)
    print(input_dir)
    for d_mod_i in range(64, d_mod + 1, 64):
        save_encoded_mod_dir = os.path.join(base_save_dir, f"d_mod_{d_mod_i}")
        os.makedirs(save_encoded_mod_dir, exist_ok=True)

        for name in os.listdir(input_dir):
            image_name = name
            file_path = os.path.join(input_dir, name)
            save_file_path = os.path.join(save_encoded_mod_dir, name)
            visualy_encode_video_file(
                file_path, save_file_path, bite_ecncode_mod, d_mod_i, seed
            )
            print(f"encoded {file_path} saved a{save_file_path}")
