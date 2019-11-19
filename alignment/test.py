import os
import subprocess

seqs = {
    'a0': 'AGTAGACCAACAGCGCTGTG',
    'a1': 'GTCGAGGAGTTATGAACGGT',
    'a10': 'ATCTCCTTGCGTTTTAAGCC',
    'a11': 'GTGTACTCAAAGCACGTACA',
    'a12': 'AAGAGAGGTAGGTAGATTAC',
    'a13': 'GTGCCCCTAAAAAGAGGAGA',
    'a14': 'TGGGCCAATTATGGATCAGT',
    'a15': 'TTAATTCGGTCACCATGTCG',
    'a16': 'CAGCTTCAGCGACAATCCGG',
    'a17': 'TTCAAAACTGACCTGTTGGG',
    'a18': 'GGTCAGGATCATTACGAGTA',
    'a19': 'CTCGCTATTCAATAGTTACG',
    'a2': 'TTTGGGTGCATTTGTTTCAA',
    'a3': 'AGGAAGATAAGGTCGTCCAT',
    'a4': 'GTAACTCCCCTTCTGGCCGG',
    'a5': 'AGTGCCTTTCGTTTTAGTTT',
    'a6': 'TGATCCAACTGTTTAATGGG',
    'a7': 'CGGAGAAAACGCCGCATTAT',
    'a8': 'ATCAGCGAATCACCGGTTTC',
    'a9': 'CCAGCCTGGCGAGCTAATAA',
    'b0': 'AATGGCCTAGATCCTACCTA',
    'b1': 'GACTTTTCCTGGCCCGTACG',
    'b10': 'AATTTGCGGAAGCATCAGGG',
    'b11': 'CGATTAGACTCGTGGTACAG',
    'b12': 'TTCGGATGGTTGCTACTCGG',
    'b13': 'TTTCCCCGTGCAGGACGCCT',
    'b14': 'ACGAGGGCTTTAGCCCGCGA',
    'b15': 'GGAGTGCTACCTATGAGGAA',
    'b16': 'GCACTAGGTGGGTGCGCCAA',
    'b17': 'CCACCCTAGGAACAGCTACC',
    'b18': 'GTCCTTACGTAGCAGGCCCG',
    'b19': 'AAGTTACTACGTCAGCCGAC',
    'b2': 'CAGACGATAGGAAAATGTGG',
    'b3': 'TACCTCTCGCGAAACCGGCT',
    'b4': 'CTCTCATCATACACCACTTC',
    'b5': 'CAAAGAATAGGGCCTTTTCA',
    'b6': 'GGGTCAGAGATTCACGCTGG',
    'b7': 'TTGGGGTGTCACTCGTCGCG',
    'b8': 'GCATGGGCTTCAAGCACGTG',
    'b9': 'GAAGAGGTGAGGGTAGCGAC'}

labels = [("a" + str(i), "b" + str(i)) for i in range(20)]
if "seq1.test" in os.listdir("."):
    os.remove("seq1.test")
if "seq2.test" in os.listdir("."):
    os.remove("seq2.test")

result_nw = "nw.results"
f = open(result_nw, "w")
f.truncate()
f.close()
result_sw = "sw.results_direction" # change output file name
f = open(result_sw, "w")
f.truncate()
f.close()

with open(result_nw, "a") as nw, open(result_sw, "a") as sw:
    for idx, val in enumerate(labels):
        a, b = val
        with open("seq1.test", "w") as s1, open("seq2.test", "w") as s2:
            s1.write(">%s\n" % a)
            s1.write("%s\n" % seqs[a])
            s2.write(">%s\n" % b)
            s2.write("%s\n" % seqs[b])
        # proc_nw = subprocess.Popen(["python3", "nwAlign.py", "seq1.test", "seq2.test"],
        #                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # nw.write("#Test: " + str(idx) + "\n" + proc_nw.communicate()[0].decode("utf-8") + "\n")
        proc_sw = subprocess.Popen(["python3", "test_sw.py", "seq1.test", "seq2.test"], # change which script to run
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        sw.write("#Test: " + str(idx) + "\n" + proc_sw.communicate()[0].decode("utf-8") + "\n")
print("Finish!")
