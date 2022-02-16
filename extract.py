import csv
import glob
import math
import os
from collections import defaultdict
from multiprocessing import Pool
from typing import Generator, List, Tuple

import nori
from absl import app, flags, logging
from nori import Dictionary, NoriTokenizer
from tqdm import tqdm

FLAGS = flags.FLAGS
flags.DEFINE_string("corpus", "corpus", help="corpus directory")
flags.DEFINE_string("left_output", "entropy-table-left.csv", help="left output")
flags.DEFINE_string("right_output", "entropy-table-right.csv", help="right output")
flags.DEFINE_integer("max_rows", 1000, "max rows")
flags.DEFINE_integer("n_files", 1, "n_files")

SUFFIX_INDICATOR = "##"

dictionary_path = os.path.join(
    os.path.dirname(nori.__file__),
    "dictionary",
    "latest-dictionary.nori",
)
logging.debug(f"dictionary path: {dictionary_path}")

dictionary = Dictionary()
dictionary.load_prebuilt_dictionary(dictionary_path)
tokenizer = NoriTokenizer(dictionary)


def main(argv):
    files = glob.glob(os.path.join(FLAGS.corpus, "*"))[: FLAGS.n_files]
    logging.info(f"Found {len(files)} files, files[:3]: {files[:3]}")

    left_side_freq = defaultdict(lambda: defaultdict(int))
    right_side_freq = defaultdict(lambda: defaultdict(int))

    with Pool() as pool:
        for filename in tqdm(files, position=0, desc="file"):
            for left_results, right_results in pool.imap_unordered(
                _tokenize_and_add_space_info,
                tqdm(_read_file(filename), position=1, desc="line"),
                chunksize=1_000,
            ):
                for key, token in left_results:
                    left_side_freq[key][token] += 1

                for key, token in right_results:
                    right_side_freq[key][token] += 1

    def _dump_entropy(freq_dictionary, filename):
        rows = []
        for term, occurances in tqdm(
            freq_dictionary.items(),
            desc="calculate entropy...",
        ):
            n_total = sum(v for _, v in occurances.items())
            if n_total == 1 or len(occurances) == 1:
                continue
            if " " not in term:
                continue

            entropy = 0.0
            for _, v in occurances.items():
                freq = v / float(n_total)
                entropy -= freq * math.log(freq)
            rows.append({"term": term, "entropy": entropy})
        rows = sorted(rows, key=lambda x: x["entropy"], reverse=True)

        with open(filename, "w") as f:
            writer = csv.DictWriter(f, fieldnames=["term", "entropy"])
            writer.writeheader()
            writer.writerows(rows[: FLAGS.max_rows])

    _dump_entropy(left_side_freq, FLAGS.left_output)
    _dump_entropy(right_side_freq, FLAGS.right_output)


def _read_file(filename: str) -> Generator[str, None, None]:
    """Read file content of given filename

    This function will skip empty line

    Returns:
        Generator object that yield each line
    """
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            yield line


def _tokenize_and_add_space_info(
    line: str,
) -> Tuple[List[List[Tuple[str, str]]], List[List[Tuple[str, str]]]]:
    """tokenize line and return tokens like BertTokenizer

    Example:
        word branching (original line)
        -> wo rd branch ing (tokenization output)
        -> wo ##rd branch ##ing (output of this function)
    """
    tokens = tokenizer.tokenize(line).tokens[1:-1]  # remove BOS/EOS
    next_offset = -1
    results = []
    for token in tokens:
        if next_offset != token.offset:
            results.append([(token.surface, token)])
        else:
            results[-1].append((SUFFIX_INDICATOR + token.surface, token))
        next_offset = token.offset + token.length

    left_results = []
    right_results = []
    for tokens in results:
        num_tokens = len(tokens)

        if num_tokens == 1:
            continue

        for i in range(1, num_tokens):
            if any(p.startswith("S") for token in tokens[:i] for p in token[1].postag):
                continue
            block_list = {"E", "J"}
            if any(p in block_list for p in tokens[i - 1][1].postag):
                continue

            key = " ".join(t[0] for t in tokens[:i])
            left_results.append((key, tokens[i][0]))

        for i in range(1, num_tokens):
            if any(p.startswith("S") for token in tokens[-i:] for p in token[1].postag):
                continue

            key = " ".join(t[0] for t in tokens[-i:])
            right_results.append((key, tokens[-i - 1][0]))

    return left_results, right_results


if __name__ == "__main__":
    app.run(main)
