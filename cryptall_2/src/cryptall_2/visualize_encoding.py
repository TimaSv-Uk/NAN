import cv2
import numpy as np

import wave

from .encode_decode import encode_bites_rand


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
    NOTE: saved video 8-10 times larger then original and function preaty slow
    not recommended to use for large videos
    """
    if save_encoded_file_path.lower().endswith(".mp4"):
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    else:
        if not save_encoded_file_path.lower().endswith(".avi"):
            save_encoded_file_path += ".avi"
        fourcc = cv2.VideoWriter_fourcc(*"XVID")

    cap = cv2.VideoCapture(file_path)
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(
        save_encoded_file_path, fourcc, fps, (frameWidth, frameHeight)
    )
    fc = 0
    ret = True
    while ret:
        ret, frame = cap.read()

        if not ret:
            break

        frame_vector = frame.flatten()
        encoded_vector = encode_bites_rand(frame_vector, bite_ecncode_mod, d_mod, seed)
        encoded_frame = encoded_vector.reshape(frame.shape)
        out.write(encoded_frame)
        fc += 1
        if fc % 50 == 0:
            print(f"Processed {fc} frames")

    out.release()
    print(f"Video saved successfully to: {save_encoded_file_path}")
    return save_encoded_file_path


def visualy_encode_audio_wav_file(
    file_path: str,
    save_encoded_file_path: str,
    bite_ecncode_mod: int = 256,
    d_mod: int = 128,
    seed: int = 42,
):
    """
    Reads WAV file, encodes it with a visual-like encoding algorithm,
    and saves it as a new WAV file.
    """
    with wave.open(file_path, "rb") as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        frames = wf.readframes(n_frames)

    # NOTE: encode_bites_rand converst to np.uint8
    dtype_map = {1: np.uint8, 2: np.int16, 4: np.int32}

    if sampwidth not in dtype_map:
        raise ValueError(f"Unsupported sample width: {sampwidth}")
    audio_array = np.frombuffer(frames, dtype=dtype_map[sampwidth])

    audio_vector = audio_array.flatten()
    encoded_vector = encode_bites_rand(audio_vector, bite_ecncode_mod, d_mod, seed)
    encoded_audio = encoded_vector.reshape(audio_array.shape)

    with wave.open(save_encoded_file_path, "wb") as wf:
        wf.setnchannels(n_channels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(framerate)
        wf.writeframes(encoded_audio.tobytes())

    print(f"Audio saved successfully to: {save_encoded_file_path}")
    return save_encoded_file_path
