import sys
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sbn

# Open file for reading
reads = open(sys.argv[1], "r")
# Skip first line to read bases
reads.readline()
line = reads.readline()
base_count = {"A": 0, "G": 0, "T": 0, "C": 0}
# Iterate through file reading every four lines and counting bases
while line != "":
    for x in range(len(line)):
        if line[x] == "A":
            base_count["A"] += 1
        elif line[x] == "G":
            base_count["G"] += 1
        elif line[x] == "T":
            base_count["T"] += 1
        else:
            base_count["C"] += 1
    for x in range(3):
        line = reads.readline()
# Print counts of each base
for base, count in base_count.items():
    print("%s count: %d" % (base, count))
# Close file after reading
reads.close()
# Write data to csv file for seaborn use
fields = ["Base", "Count"]
data = [["A", base_count['A']], ["G", base_count["G"]],["T", base_count["T"]], ["C", base_count["C"]]]
filename = "results.csv"
with open(filename, 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(fields)
    csv_writer.writerows(data)
data_set = pd.read_csv(filename)
sbn.barplot(x="Base", y="Counts", data=data_set)
plt.show()
