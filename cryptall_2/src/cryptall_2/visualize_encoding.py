import cv2
import numpy as np

from .helpers import encode_bites_rand


def visualy_encode_image_file(
    file_path: str,
    save_encoded_file_path: str,
    bite_ecncode_mod: int = 256,
    d_mod: int = 128,
    seed: int = 42,
):
    """
    Saves encoded file that can be read and visualy encryption algirithm
    """

    img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

    pixels = np.array(img)
    pixels_vector = pixels.flatten()

    pixels_vector = encode_bites_rand(pixels_vector, bite_ecncode_mod, d_mod, seed)

    encoded_pixels = pixels_vector.reshape(np.shape(pixels))

    cv2.imwrite(save_encoded_file_path, encoded_pixels)


def visualy_encode_video_file(
    file_path: str,
    save_encoded_file_path: str,
    bite_ecncode_mod: int = 256,
    d_mod: int = 128,
    seed: int = 42,
):
    if not save_encoded_file_path.lower().endswith((".mp4", ".avi")):
        save_encoded_file_path += ".avi"

    cap = cv2.VideoCapture(file_path)
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(
        save_encoded_file_path, fourcc, fps, (frameWidth, frameHeight)
    )

    fc = 0
    ret = True
    while ret:
        ret, frame = cap.read()
        if not ret:
            break

        # Flatten and encode the frame
        frame_vector = frame.flatten()
        encoded_vector = encode_bites_rand(frame_vector, bite_ecncode_mod, d_mod, seed)
        encoded_frame = encoded_vector.reshape(frame.shape)

        out.write(encoded_frame)
        fc += 1
        if fc % 50 == 0:
            print(f"Processed {fc} frames")

    cap.release()
    out.release()
    print(f"Video saved successfully to: {save_encoded_file_path}")
    return save_encoded_file_path
