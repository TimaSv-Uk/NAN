import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

import time
from pathlib import Path

from cryptall_2.encode_decode import encode_bites_rand, load_file_to_bites

BASE_DIR = Path(__file__).parent.parent.parent
TEST_FILES_DIR = BASE_DIR / "test_files"
SAVE_FILES_DIR = BASE_DIR / "test_results"

# List of files to analyze
file_paths = [
    TEST_FILES_DIR / "data2.txt",
    TEST_FILES_DIR / "img.jpg",
    TEST_FILES_DIR / "vid_31mb.mp4",
    TEST_FILES_DIR / "csv_123mb.csv",
]


def get_file_data(file_paths: list[str]):
    char_ecncode_mod = 256
    d_mod = 128
    seed = 42
    execution_time_data = []

    for path_str in file_paths:
        path = Path(path_str)
        if not path.exists():
            print(f"File not found: {path}")
            continue

        file_bites: np.ndarray = load_file_to_bites(path)
        text_len = len(file_bites)
        print(text_len)

        start_time = time.perf_counter()
        encode_bites_rand(file_bites, char_ecncode_mod, d_mod, seed)
        end_time = time.perf_counter()
        execution_time_data.append(
            {
                "file": path.name,
                "bite_len": text_len,
                "execution_time": end_time - start_time,
            }
        )

    return execution_time_data


def plot_bite_length_chart(file_paths: list[str]) -> None:
    data = get_file_data(file_paths)
    df = pd.DataFrame(data)
    sns.set(style="whitegrid")

    df["bite_len_MB"] = df["bite_len"] / 1_000_000
    # lmplot to show time complexity vs file size
    sns.lmplot(
        data=df,
        x="bite_len_MB",
        y="execution_time",
        hue="file",
        markers="o",
        ci=None,
        aspect=1.5,
        height=5,
    )
    plt.title("Execution Time vs File Byte Length")
    plt.xlabel("File Byte Length (MB)")
    plt.ylabel("Execution Time (s)")
    plt.savefig(
        SAVE_FILES_DIR / "execution_times_by_bite_length.pdf",
        format="pdf",
        bbox_inches="tight",
    )
    plt.close()


if __name__ == "__main__":
    plot_bite_length_chart(file_paths)
