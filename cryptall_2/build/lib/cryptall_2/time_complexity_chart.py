import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import time
import numpy as np
from pathlib import Path
from helpers import encode_assignment5, load_file_to_bites


# List of files to analyze
file_paths = [
    "test_files/data2.txt",
    "test_files/img.jpg",
    "test_files/vid_31mb.mp4",
    "test_files/csv_123mb.csv",
]


def get_file_data(file_paths: list[str]):
    char_ecncode_mod = 256
    d_mod = 128
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
        encode_assignment5(file_bites, char_ecncode_mod, d_mod)
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
    plt.savefig("execution_times_by_bite_length.pdf", format="pdf", bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    plot_bite_length_chart(file_paths)
