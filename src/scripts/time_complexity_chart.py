import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

import time
from pathlib import Path

from cryptall_2.encode_decode import (
    encode_bites_rand,
    load_file_to_bites,
    encode_file,
    decode_file,
)

BASE_DIR = Path(__file__).parent.parent.parent

TEST_FILES_DIR = BASE_DIR / "tests/test_files"
SAVE_FILES_DIR = BASE_DIR / "tests/test_results"

SEED = 42
# List of files to analyze
file_paths = [
    TEST_FILES_DIR / "data.txt",
    TEST_FILES_DIR / "data2.txt",
    TEST_FILES_DIR / "img.jpg",
    TEST_FILES_DIR / "vid_27mb.mp4",
    TEST_FILES_DIR / "csv_100mb.csv",
    # TEST_FILES_DIR / "1gb_zip.zip",
]


def get_decode_file_data(file_paths: list[str]):
    execution_time_data = []

    for path_str in file_paths:
        path = Path(path_str)
        if not path.exists():
            print(f"File not found: {path}")
            continue

        encoded_file_path = (
            SAVE_FILES_DIR / "encoded" / f"{path.stem}_encoded{path.suffix}"
        )
        decoded_file_path = (
            SAVE_FILES_DIR / "decoded" / f"{path.stem}_decoded{path.suffix}"
        )
        file_bites: np.ndarray = load_file_to_bites(path)
        text_len = len(file_bites)
        print(text_len)

        start_time = time.perf_counter()

        decode_file(encoded_file_path, decoded_file_path, SEED)
        end_time = time.perf_counter()
        execution_time_data.append(
            {
                "file": path.name,
                "bite_len": text_len,
                "execution_time": end_time - start_time,
            }
        )

    return execution_time_data


def get_encode_file_data(file_paths: list[str]):
    execution_time_data = []

    for path_str in file_paths:
        path = Path(path_str)
        if not path.exists():
            print(f"File not found: {path}")
            continue

        encoded_file_path = (
            SAVE_FILES_DIR / "encoded" / f"{path.stem}_encoded{path.suffix}"
        )
        # decoded_file_path = (
        #     SAVE_FILES_DIR / "decoded" / f"{path.stem}_decoded{path.suffix}"
        # )
        file_bites: np.ndarray = load_file_to_bites(path)
        text_len = len(file_bites)
        print(text_len)

        start_time = time.perf_counter()

        encode_file(path, encoded_file_path, SEED)
        end_time = time.perf_counter()
        execution_time_data.append(
            {
                "file": path.name,
                "bite_len": text_len,
                "execution_time": end_time - start_time,
            }
        )

    return execution_time_data


def plot_encode_bite_length_chart(file_paths: list[str]) -> None:
    data = get_encode_file_data(file_paths)
    df = pd.DataFrame(data)
    sns.set(style="whitegrid")

    df["bite_len_MB"] = df["bite_len"] / 1_000_000
    plt.figure(figsize=(10, 6))
    sns.lmplot(
        data=df,
        x="bite_len_MB",
        y="execution_time",
        ci=None,
        # hue="file",
        markers="o",
        scatter_kws={"s": 150},  # Bigger points
        line_kws={"linewidth": 2},  # More visible regression line
        # aspect=1.5,
        # height=5,
    )
    plt.title("ENCODE Execution Time vs File Byte Length")
    plt.xlabel("File Byte Length (MB)")
    plt.ylabel("Execution Time (s)")
    plt.savefig(
        SAVE_FILES_DIR / "ENCODE_file_execution_times_by_bite_length.pdf",
        format="pdf",
        bbox_inches="tight",
    )
    plt.close()


def plot_decode_bite_length_chart(file_paths: list[str]) -> None:
    data = get_decode_file_data(file_paths)
    df = pd.DataFrame(data)
    sns.set(style="whitegrid")

    df["bite_len_MB"] = df["bite_len"] / 1_000_000
    plt.figure(figsize=(10, 6))
    sns.lmplot(
        data=df,
        x="bite_len_MB",
        y="execution_time",
        ci=None,
        # hue="file",
        markers="o",
        scatter_kws={"s": 150},  # Bigger points
        line_kws={"linewidth": 2},  # More visible regression line
        # aspect=1.5,
        # height=5,
    )
    plt.title("DECODE Execution Time vs File Byte Length")
    plt.xlabel("File Byte Length (MB)")
    plt.ylabel("Execution Time (s)")
    plt.savefig(
        SAVE_FILES_DIR / "DECODE_file_execution_times_by_bite_length.pdf",
        format="pdf",
        bbox_inches="tight",
    )
    plt.close()


if __name__ == "__main__":
    plot_encode_bite_length_chart(file_paths)
    plot_decode_bite_length_chart(file_paths)
