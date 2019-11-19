import random
import os
import sys
import subprocess
import time
import argparse

if 'test.out' in os.listdir("."):
    os.remove('test.out')
    os.remove('test.join.out')

chromosomes = [
    "chr1",
    "chr10",
    "chr11",
    "chr12",
    "chr13",
    "chr14",
    "chr15",
    "chr16",
    "chr17",
    "chr18",
    "chr19",
    "chr2",
    "chr20",
    "chr21",
    "chr22",
    "chr3",
    "chr4",
    "chr5",
    "chr6",
    "chr7",
    "chr8",
    "chr9",
    "chrX",
    "chrY"
]


def generate_random_bed(file_name, file_size):
    with open(file_name, "w") as f:
        for chromosome in chromosomes:
            starts = [random.randint(1000, 10000000) for _ in
                      range(random.randint(10 ** file_size, 10 ** (file_size + 1)))]
            starts.sort()
            lengths = [round(random.expovariate(0.05)) for _ in range(len(starts))]
            for start, length in zip(starts, lengths):
                f.write("%s\t%d\t%d\t%s\t%s\n" % (chromosome, start, start + length, "0", "+"))


def main():
    if not "draft3.py" in os.listdir("."):
        raise FileNotFoundError("No script detected")
    if args.default:
        file1, file2 = "TE.bed", "Intron.bed"
        if not file1 in os.listdir(".") or not file2 in os.listdir("."):
            raise FileNotFoundError("No input file, check again")
    else:
        file1, file2 = "test1.bed", "test2.bed"
        if not "test1.bed" in os.listdir("."):
            random.seed(args.seed)
            generate_random_bed("test1.bed", args.s)
        if not "test2.bed" in os.listdir("."):
            random.seed(2 * args.seed)
            generate_random_bed("test2.bed",args.s)


    print("start execution")
    start = time.time()
    subprocess.run(["python3", "draft3.py", "-i1", file1, "-i2", file2, "-m", str(args.m), "-o", "test.out"])
    print("without join flag, script takes about %.2f seconds" % (time.time() - start))
    sys.stdout.write("number of lines: ")
    sys.stdout.flush()
    subprocess.Popen(["wc", "-l", "test.out"])
    start = time.time()
    subprocess.run(
        ["python3", "draft3.py", "-i1", file1, "-i2", file2, "-j", "-m", str(args.m), "-o", "test.join.out"])
    print("with join flag, script takes about %.2f seconds" % (time.time() - start))
    sys.stdout.write("number of lines: ")
    sys.stdout.flush()
    subprocess.Popen(["wc", "-l", "test.join.out"])
    time.sleep(2)
    print("all finish!")


if __name__ == "__main__":
    desc = """
    if --default flag is not provided, then script will 
    use test1.bed and test2.bed as input if they do not exist.
    output file will be test.out and test.join.out.
    delete test*.bed to generate bed file with different size.
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--default', action="store_true",
                        help="use default file, TE & Intron, as input, else use test1 & test2")
    parser.add_argument('--seed', default=1234, type=int, help="random seed, must be int, default 1234")
    parser.add_argument('-m', default=80, type=int, help="percent, default 80")
    parser.add_argument('-s', default=4, choices=[2, 3, 4, 5, 6],
                        help="test file size, bigger indicates larger file. default=4")
    args = parser.parse_args()
    main()
