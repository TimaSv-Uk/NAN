from cryptall_2.visualize_encoding import (
    visualy_encode_image_file,
    visualy_encode_video_file,
    visualy_encode_audio_wav_file,
)

if __name__ == "__main__":
    bite_ecncode_mod: int = 256
    d_mod: int = 128
    seed: int = 42

    image_name = "img.jpg"
    image_name = "big_img.jpg"
    image_file_path = f"test_files/{image_name}"
    image_save_file_path = f"test_files/visual_encoded_{image_name}"

    visualy_encode_image_file(
        image_file_path, image_save_file_path, bite_ecncode_mod, d_mod, seed
    )
    print(f"encoded {image_file_path} saved a{image_save_file_path}")

    vid_name = "vid_31mb.mp4"
    vid_file_path = f"test_files/{vid_name}"
    vid_save_file_path = f"test_files/visual_encoded_{vid_name}"

    visualy_encode_video_file(
        vid_file_path, vid_save_file_path, bite_ecncode_mod, d_mod, seed
    )

    vid_name = "vid_31mb.mp4"
    vid_file_path = f"test_files/{vid_name}"
    vid_save_file_path = f"test_files/visual_encoded_{vid_name}"

    visualy_encode_audio_wav_file()
