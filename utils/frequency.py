from collections import defaultdict

def print_top_frequencies(frequencies, top_n=50):
    sorted_freq = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    for word, freq in sorted_freq[:top_n]:
        print(f"{word} -> {freq}")


def write_top_frequencies(frequencies, file,top_n=50):
    sorted_freq = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    for word, freq in sorted_freq[:top_n]:
        file.write(f"{word} -> {freq}\n")