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
    """
    Saves encoded file that can be read and visualy encryption algirithm
    """
    cap = cv2.VideoCapture(file_path)
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    buf = np.empty((frameCount, frameHeight, frameWidth, 3), dtype=np.uint8)

    fc = 0
    ret = True

    while fc < frameCount and ret:
        ret, buf[fc] = cap.read()
        fc += 1
    cap.release()

    video_vector = buf.flatten()

    video_vector = encode_bites_rand(video_vector, bite_ecncode_mod, d_mod, seed)

    encoded_video = video_vector.reshape(np.shape(buf))

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(
        save_encoded_file_path, fourcc, frameCount, (frameWidth, frameHeight)
    )
    # Write frames to the video file
    for frame in encoded_video:
        out.write(frame)

    out.release()
