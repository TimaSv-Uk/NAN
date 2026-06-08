from pathlib import Path
import unittest
import random
import time

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from cryptall_2.precompute_multiplication import precompute_sudo512_mod, load_sudo512_mod
from cryptall_2.encode_decode import (
    encode_bites,
    decode_bites,
    encode_bites_rand,
    encode_bites_full,
    encode_bites_ring,
    decode_bites_ring,
    remove_noise,
    encode_bites_f8,
    decode_bites_f8,
    encode_bites_sudo512_mod,
    decode_bites_sudo512_mod
)
from cryptall_2.core.main_modulo import randomize_d_mod
from cryptall_2.helpers import (
    bites_sameness_percentage,
    load_file_to_bites,
    sudo_random_array,
)


class BaseEncodeDecodeTest:
    """
    Base class for polymorphic testing of encode/decode algorithms.
    Do NOT run this class directly. Run its subclasses.
    """

    def setUp(self):
        self.char_mod = 256
        self.d_mod = 128
        self.seed = 50
        self.test_file_dir = Path("./tests/test_files/")
        self.test_results_dir = Path("./tests/test_results/")
        self.file_names = {
            "txt": "data2.txt",
            "img": "img.jpg",
            "vid": "vid_27mb.mp4",
            "csv": "csv_100mb.csv",
        }
        # To store data for the graph
        self.perf_results = []
        # NOTE: Child classes MUST define:
        # self.encode_func
        # self.decode_func
        # self.alg_name (used for saving result files)

    def test_encode_decode_consistency(self):
        """Test that encoding followed by decoding restores the original bites."""
        file_bites = load_file_to_bites(
            f"{self.test_file_dir}/{self.file_names['txt']}"
        )
        encoded = self.encode_func(file_bites, self.char_mod, self.d_mod, self.seed)
        decoded = self.decode_func(encoded, self.char_mod, self.d_mod, self.seed)
        self.assertTrue(np.array_equal(file_bites, decoded))

    def _record_perf(self, file_name, bite_len, exec_time, operation):
        self.perf_results.append(
            {
                "algorithm": self.alg_name,
                "file": file_name,
                "bite_len_MB": bite_len / 1_000_000,
                "execution_time": exec_time,
                "operation": operation,
            }
        )

    def test_execution_performance(self):
        """Measures time and stores data for plotting."""
        for label, file_name in self.file_names.items():
            path = self.test_file_dir / file_name
            if not path.exists():
                continue

            file_bites = load_file_to_bites(str(path))
            bite_len = len(file_bites)

            # Measure Encoding
            start = time.perf_counter()
            encoded = self.encode_func(file_bites, self.char_mod, self.d_mod, self.seed)
            self._record_perf(
                file_name, bite_len, time.perf_counter() - start, "Encode"
            )

            # Measure Decoding
            start = time.perf_counter()
            self.decode_func(encoded, self.char_mod, self.d_mod, self.seed)
            self._record_perf(
                file_name, bite_len, time.perf_counter() - start, "Decode"
            )

        # Trigger plot generation after collecting data
        self.plot_complexity_graphs()

    def plot_complexity_graphs(self):
        """Generates regression plots for the specific algorithm."""
        if not self.perf_results:
            return

        df = pd.DataFrame(self.perf_results)
        sns.set_theme(style="whitegrid")

        for op in ["Encode", "Decode"]:
            subset = df[df["operation"] == op]

            plt.figure(figsize=(10, 6))
            g = sns.lmplot(
                data=subset,
                x="bite_len_MB",
                y="execution_time",
                ci=None,
                markers="o",
                scatter_kws={"s": 150, "alpha": 0.7},
                line_kws={"linewidth": 2, "color": "red" if op == "Encode" else "blue"},
            )

            plt.title(f"{self.alg_name.upper()} - {op} Complexity Analysis")
            plt.xlabel("File Size (MB)")
            plt.ylabel("Time (seconds)")

            save_path = self.test_results_dir / f"{self.alg_name}_{op}_complexity.pdf"
            plt.savefig(save_path, format="pdf", bbox_inches="tight")
            plt.close()

    def test_encode_decode_dmod0(self):
        """Test that encoding followed by decoding restores the original bites with dmod 0."""
        file_bites = load_file_to_bites(
            f"{self.test_file_dir}/{self.file_names['txt']}"
        )
        encoded = self.encode_func(file_bites, self.char_mod, 0, self.seed)
        decoded = self.decode_func(encoded, self.char_mod, 0, self.seed)
        self.assertTrue(np.array_equal(file_bites, decoded))

    def test_encode_decode_dmod1(self):
        """Test that encoding followed by decoding restores the original bites with dmod 1."""
        file_bites = load_file_to_bites(
            f"{self.test_file_dir}/{self.file_names['txt']}"
        )
        encoded = self.encode_func(file_bites, self.char_mod, 1, self.seed)
        decoded = self.decode_func(encoded, self.char_mod, 1, self.seed)
        self.assertTrue(np.array_equal(file_bites, decoded))

    def _test_file_encoding_sameness(
        self, file_key: str, encode_func, seed: int, save_prefix: str
    ):
        """Helper to test file encoding sameness and save results to a file."""
        file_path = f"{self.test_file_dir}/{self.file_names[file_key]}"
        save_path = f"{self.test_results_dir}{save_prefix}_{
            self.file_names[file_key].split('.')[0]
        }.txt"

        file_bites = load_file_to_bites(file_path)
        encoded_base = encode_func(file_bites, self.char_mod, self.d_mod, seed)

        # Deterministic check
        encoded_base2 = encode_func(file_bites, self.char_mod, self.d_mod, seed)
        self.assertTrue(np.array_equal(encoded_base, encoded_base2))

        length = len(file_bites)
        quarter_indices = [length // 4, length // 2, 3 * length // 4, length - 1]

        with open(save_path, "w", encoding="utf-8") as f:
            for i, idx in enumerate(quarter_indices, 1):
                with self.subTest(quarter=i):
                    modified_bites = file_bites.copy()
                    original_val = int(modified_bites[idx])

                    new_val = random.randint(0, 255)
                    while new_val == original_val:
                        new_val = random.randint(0, 255)
                    modified_bites[idx] = np.uint8(new_val)

                    encoded_modified = encode_func(
                        modified_bites,
                        self.char_mod,
                        self.d_mod,
                        seed + 1 if "rand" in encode_func.__name__ else seed,
                    )
                    percent = bites_sameness_percentage(encoded_base, encoded_modified)

                    # Save results to file
                    f.write(f"Quarter {i} change at index {idx}\n")
                    f.write(
                        f"Original byte: {original_val}, Modified byte: {new_val}\n"
                    )
                    f.write(f"Sameness %: {percent}%\n")
                    f.write("-" * 50 + "\n")

                    self.assertLess(percent, 100)

    def test_text_sameness_FILE_encoding(self):
        """Dynamically tests the current algorithm injected by the child class."""

        for file_label, _ in self.file_names.items():
            self._test_file_encoding_sameness(
                file_label,
                self.encode_func,
                self.seed,
                # Uses the child's algorithm name
                f"sameness_with_changed_bite_{self.alg_name}_{file_label}",
            )

    def test_execution_time(self):
        """Dynamically tests execution time for the injected algorithm."""
        for file_name in self.file_names.values():
            file_bites = load_file_to_bites(f"{self.test_file_dir}/{file_name}")
            print(f"\n--- Testing Algorithm: {self.alg_name.upper()} ---")
            print(f"File name: {file_name}")
            print(f"Generated array of size: {file_bites.shape} bytes")

            start_time = time.perf_counter()
            encoded = self.encode_func(file_bites, self.char_mod, self.d_mod, self.seed)
            execution_time = time.perf_counter() - start_time
            print(f"Encoded execution_time: {execution_time:.4f}s")

            start_time = time.perf_counter()
            decoded = self.decode_func(encoded, self.char_mod, self.d_mod, self.seed)
            execution_time = time.perf_counter() - start_time
            print(f"Decoded execution_time: {execution_time:.4f}s")

    # NOTE: takes to long to run, need to fix or uncomment when needs to be run
    def test_digest_with_no_noise(self):
        file_path = f"{self.test_file_dir}/{self.file_names['vid']}"
        file_bites = load_file_to_bites(file_path)
        number_of_digests = 10
        noise_ratio = 0.05

        encode_no_noise = self.encode_func(
            file_bites, self.char_mod, self.d_mod, self.seed
        )

        encode_with_noise = self.encode_func(
            file_bites, self.char_mod, self.d_mod, self.seed, noise_ratio
        )
        encode_with_noise = remove_noise(
            encode_with_noise, self.char_mod, self.seed, noise_ratio
        )
        self.assertFalse(np.array_equal(encode_no_noise, encode_with_noise))

        digests_no_noise = np.array_split(encode_no_noise, number_of_digests)
        digests_with_noise = np.array_split(encode_with_noise, number_of_digests)
        comparison_lines = []
        for i, (d1, d2) in enumerate(zip(digests_no_noise, digests_with_noise)):
            equal = np.array_equal(d1, d2)

            if equal:
                comparison_lines.append(f"Digest {i}: IDENTICAL\n")
            else:
                diff_count = bites_sameness_percentage(d1, d2)
                comparison_lines.append(
                    f"Digest {i}: DIFFERENT — {diff_count} bytes differ\n"
                )

        report_path = f"{self.test_results_dir}{
            self.alg_name.upper()
        }_digest_comparison_report.txt"

        with open(report_path, "w", encoding="utf-8") as f:
            f.writelines(comparison_lines)

    def _record_perf(self, file_name, bite_len, exec_time, operation):
        self.perf_results.append(
            {
                "algorithm": self.alg_name,
                "file": file_name,
                "bite_len_MB": bite_len / 1_000_000,
                "execution_time": exec_time,
                "operation": operation,
            }
        )

    def test_execution_performance(self):
        """Measures time and stores data for plotting."""
        for label, file_name in self.file_names.items():
            path = self.test_file_dir / file_name
            if not path.exists():
                continue

            file_bites = load_file_to_bites(str(path))
            bite_len = len(file_bites)

            # Measure Encoding
            start = time.perf_counter()
            encoded = self.encode_func(file_bites, self.char_mod, self.d_mod, self.seed)
            self._record_perf(
                file_name, bite_len, time.perf_counter() - start, "Encode"
            )

            # Measure Decoding
            start = time.perf_counter()
            self.decode_func(encoded, self.char_mod, self.d_mod, self.seed)
            self._record_perf(
                file_name, bite_len, time.perf_counter() - start, "Decode"
            )

        # Trigger plot generation after collecting data
        self.plot_complexity_graphs()

    def plot_complexity_graphs(self):
        """Generates regression plots for the specific algorithm."""
        if not self.perf_results:
            return

        df = pd.DataFrame(self.perf_results)
        sns.set_theme(style="whitegrid")

        for op in ["Encode", "Decode"]:
            subset = df[df["operation"] == op]

            plt.figure(figsize=(10, 6))
            g = sns.lmplot(
                data=subset,
                x="bite_len_MB",
                y="execution_time",
                ci=None,
                markers="o",
                scatter_kws={"s": 150, "alpha": 0.7},
                line_kws={"linewidth": 2, "color": "red" if op == "Encode" else "blue"},
            )

            plt.title(f"{self.alg_name.upper()} - {op} Complexity Analysis")
            plt.xlabel("File Size (MB)")
            plt.ylabel("Time (seconds)")

            save_path = (
                Path(self.test_results_dir) / f"{self.alg_name}_{op}_complexity.pdf"
            )

            plt.savefig(save_path, format="pdf", bbox_inches="tight")
            plt.close()


# NOTE: ALGORITHM IMPLEMENTATIONS (These are actually run by pytest)


class TestStandardAlgorithm(BaseEncodeDecodeTest, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.encode_func = encode_bites
        self.decode_func = decode_bites

        self.test_results_dir = "./tests/test_results_standard/"
        Path(self.test_results_dir).mkdir(parents=True, exist_ok=True)
        self.alg_name = "original_d_mod"


class TestF8Algorithm(BaseEncodeDecodeTest, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.encode_func = encode_bites_f8
        self.decode_func = decode_bites_f8

        self.test_results_dir = "./tests/test_results_f8/"
        Path(self.test_results_dir).mkdir(parents=True, exist_ok=True)
        self.alg_name = "f8_mod"


class TestSUDO512MOD_Algorithm(BaseEncodeDecodeTest, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.encode_func = encode_bites_sudo512_mod
        self.decode_func = decode_bites_sudo512_mod

        self.test_results_dir = "./tests/test_results_sudo521_mod/"
        Path(self.test_results_dir).mkdir(parents=True, exist_ok=True)
        self.alg_name = "sudo521_mod"


#
# class TestRingAlgorithm(BaseEncodeDecodeTest, unittest.TestCase):
#     def setUp(self):
#         super().setUp()
#         self.encode_func = encode_bites_ring
#         self.decode_func = decode_bites_ring
#
#         self.test_results_dir = "./tests/test_results_ring/"
#         Path(self.test_results_dir).mkdir(parents=True, exist_ok=True)
#         self.alg_name = "ring"


# NOTE: HELPER / MATH TESTS (Completely separated from encoding tests)


class TestHelpers(unittest.TestCase):
    def setUp(self):
        self.d_mod = 128
        self.seed = 50

    def test_randomized_d_mod_changes_order(self):
        """Check that randomize_d_mod changes the default sequence."""
        arr_range = np.arange(self.d_mod)
        randomized = randomize_d_mod(self.d_mod, self.seed)
        self.assertFalse(np.array_equal(arr_range, randomized))

    def test_insert_rand_array(self):
        random_array_length = 3
        random_array = sudo_random_array(random_array_length, 256, self.seed, np.uint8)
        original_arr = [1, 2, 4]
        new_arr = np.append(random_array, original_arr)

        self.assertEqual(len(new_arr) - 3, random_array_length)
        self.assertTrue(np.array_equal(original_arr, new_arr[random_array_length:]))

    def test_precompute_256_sudo512(self):
        precompute_sudo512_mod()
        print(load_sudo512_mod())


if __name__ == "__main__":
    """
    To run all test
    uv run pytest tests/tests.py

    To run selected test
    uv run pytest -s tests/tests.py::TestMathUtils::test_encode_decode_dmod1
    """

    unittest.main()
