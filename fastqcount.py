import sys
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from docopt import docopt
usage = '''
FastQ Data Analyzer

Usage:
    fastq.py <data> <results> <graphs> [<start_pos>[(- <end_pos>)]]...
    fastq.py -h | --help
    
Arguments:
    data    name of file or path to file containing fastq data
    results name of or path to new xlsx file containing overall base counts and positional base frequencies if applicable
    graphs  name of or path to new file containing barplot of total base counts and distribution of read length sizes
    start_pos  either single base or starting position of range of positions for positional base frequencies to be displayed (enter individual bases after ranges!)
    end_pos  end position of range of positions for positional base frequencies to be displayed 
'''

args = docopt(usage)

reads = 0
base_count = {"A": 0, "G": 0, "T": 0, "C": 0}
position_count = {}
positions = []
read_lengths = []

# Open file for reading and iterate through file reading every four lines and counting bases
with open(args['<data>']) as fp:
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
# Close file after reading
fp.close()

# Collects positions from command line (if applicable) and stores corresponding positional base frequencies as data frame
for i in range(0, len(args['<start_pos>'])):
    if args['<end_pos>'] and i < len(args["<end_pos>"]):
        if args['<end_pos>'][i] == args["<start_pos>"][i]:
            if args["<start_pos>"][i] not in positions:
                positions.append(int(args["<start_pos>"][i]))
        elif args['<end_pos>'][i] < args["<start_pos>"][i]:
            r1, r2 = int(args["<end_pos>"][i]), int(args["<start_pos>"][i])
            while r1 < r2 + 1:
                if r1 not in positions:
                    positions.append(r1)
                r1 += 1
        else:
            r1, r2 = int(args["<start_pos>"][i]), int(args["<end_pos>"][i])
            while r1 < r2 + 1:
                if r1 not in positions:
                    positions.append(r1)
                r1 += 1
    else:
        if args["<start_pos>"][i] not in positions:
            positions.append(int(args["<start_pos>"][i]))
positions.sort()
for pos in positions:
    if pos < 0:
        positions.remove(pos)

# Trim position count dictionary to contain only desired positions
for key in list(position_count.keys()):
    if key not in positions:
        del position_count[key]

# Change base count data to a dataframe to plot as a barplot and write to xlsx file for storage
bcount_dframe_dict = {"Base": ["A", "G", "T", "C"], "Count": [base_count["A"], base_count["G"], base_count["T"], base_count["C"]]}
bcount_dframe = pd.DataFrame(bcount_dframe_dict)
# Change position count data to a dataframe to write to xlsx file for storage
pcount_dframe = pd.DataFrame(position_count)
# Change number of reads to a dataframe to write to xlsx file for storage
rcount_dframe = pd.DataFrame({"Number of Reads": reads}, index=[0])

# Write data to xlsx file
filename = args['<results>']
with pd.ExcelWriter(filename) as writer:
    rcount_dframe.to_excel(writer, sheet_name="Number of Reads")
    bcount_dframe.to_excel(writer, sheet_name="Total Base Counts")
    pcount_dframe.to_excel(writer, sheet_name="Positional Base Counts")


# Create total base count graphs and read length size distribution and store as pdf
with PdfPages(args['<graphs>']) as pdf_pages:
    figure1 = plt.figure(1)
    barplot = sns.barplot(x="Base", y="Count", data=bcount_dframe)
    barplot.set_title("Total Base Counts Among All Reads")
    pdf_pages.savefig(figure1)
    figure2 = plt.figure(2)
    distribution = sns.lineplot(x="Length", y="Count", data=pd.DataFrame(read_lengths))
    distribution.set_title("Distribution of Read Length Sizes")
    pdf_pages.savefig(figure2)
