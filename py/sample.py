#!python
import argparse
import codecs
import random
import sys

from tqdm import tqdm


def reservoir_sampling(k, verbose=False):
    reservoir = []
    for i, line in tqdm(enumerate(sys.stdin), ncols=80, disable=(not verbose)):
        if i < k:
            # Fill the reservoir initially with the first k lines
            reservoir.append(line.strip())
        else:
            # Randomly replace elements in the reservoir with decreasing probability
            j = random.randint(0, i)
            if j < k:
                reservoir[j] = line.strip()
    return reservoir


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", metavar="FILE", help="Input filename <default: stdin>")
    parser.add_argument("--output", "-o", metavar="FILE", help="Output filename <default: stdout>")
    parser.add_argument("--sample", "-s", type=int, help="Sample size")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show progress")
    args = parser.parse_args()

    if args.input:
        sys.stdin = codecs.open(args.input, "r", encoding="utf-8")
    else:
        sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())

    if args.output:
        sys.stdout = codecs.open(args.output, "w", encoding="utf-8")
    else:
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

    for line in reservoir_sampling(args.sample, verbose=args.verbose):
        print(line)
