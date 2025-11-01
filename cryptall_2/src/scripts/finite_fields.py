from libnum import has_sqrtmod_prime_power, has_sqrtmod, sqrtmod_prime_power
import matplotlib.pyplot as plt


def main():
    xs = []
    ys = []

    mod = 255

    for x in range(0, mod):
        if has_sqrtmod_prime_power(x, mod, 1):
            for root in sqrtmod_prime_power(x, mod, 1):
                xs.append(x)
                ys.append(root)
                print(f"{x} - {root}")
    plt.scatter(xs, ys)
    plt.show()


if __name__ == "__main__":
    main()
