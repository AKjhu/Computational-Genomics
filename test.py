import sys
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#learn how to use
#import docopt

reads = 0
base_count = {"A": 0, "G": 0, "T": 0, "C": 0}
position_count = {}
read_lengths = []

# Open file for reading and iterate through file reading every four lines and counting bases
with open(sys.argv[1]) as fp:
    for line in fp:
        seq = fp.readline().rstrip()
        reads += 1
        fp.readline()
        qual = fp.readline()

        seqlen = len(seq)
        if next((len for len in read_lengths if len["Length"] == seqlen), None) not in read_lengths:
            read_lengths.append({"Length": seqlen, "Count": 1})
        else:
            (next((len for len in read_lengths if len["Length"] == seqlen), None))["Count"] += 1

        for pos in range(seqlen):
            if pos not in position_count:
                position_count[pos] = {"A": 0, "G": 0, "T": 0, "C": 0}
            base_count[seq[pos]] += 1
            position_count[pos][seq[pos]] += 1


# Print counts of each base and number of reads
for base, count in base_count.items():
    print("%s count: %d" % (base, count))
print("Number of reads: %d" % reads)
# Close file after reading
fp.close()

# Write base count data to csv file for storage
fields = ["Base", "Count"]
data = [["A", base_count['A']], ["G", base_count["G"]], ["T", base_count["T"]], ["C", base_count["C"]]]
filename = "results.csv"
with open(filename, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(fields)
    csv_writer.writerows(data)
# Change base count data to a dataframe to plot as a barplot
bcount_dframe_dict = {"Base": ["A", "G", "T", "C"], "Count": [base_count["A"], base_count["G"], base_count["T"], base_count["C"]]}
bcount_dframe = pd.DataFrame(bcount_dframe_dict)
sns.barplot(x="Base", y="Count", data=bcount_dframe)
plt.show()

# Convert read length data to univariate list to plot as histogram
# Look at something that can read bigger datasets; loop can use too much memory
# Use a scatterplot?

sns.distplot(pd.DataFrame(read_lengths))
plt.show()
