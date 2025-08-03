import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import time
import random
import string

from task2 import get_encoded_text


def randomtext(length):
    return "".join(random.choice(string.printable) for i in range(length))


def get_data():
    char_ecncode_mod = 256

    execution_time_based_on_mod_and_text = []

    i = 1
    while i <= 10001:
        text = randomtext(i)

        d_mod = 8
        while d_mod < 128 + 1:
            start_time = time.perf_counter()
            encoded_text1 = get_encoded_text(text, char_ecncode_mod, d_mod)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            execution_time_based_on_mod_and_text.append(
                {
                    "text_len": len(text),
                    "d_mod": d_mod,
                    "execution_time": execution_time,
                }
            )
            d_mod += 12

        i += 1000

    return execution_time_based_on_mod_and_text


def plot_time_complexity_chart() -> None:
    df = pd.DataFrame(get_data())
    sns.set(style="whitegrid")
    plot = sns.lmplot(
        data=df,
        x="text_len",
        hue="d_mod",
        y="execution_time",  # Separate regression lines per group
        markers="o",
        ci=None,  # No confidence interval (optional)
        aspect=1.5,  # Wider plot
        height=5,
    )
    plt.title("Execution Time vs Text Length")
    plt.xlabel("Text Length")
    plt.ylabel("Execution Time (s)")
    plt.savefig("execution_times.pdf", format="pdf", bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    plot_time_complexity_chart()
