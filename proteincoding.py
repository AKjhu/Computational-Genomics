import pysam
import gffutils
from docopt import docopt

usage = '''
Protein Coding Read Filter

Usage:
    proteincoding.py <input> <gtf> <result>
    proteincoding.py -h | --help
    
Arguments:
    input   Name of file or path to file containing reads to be filtered
    gtf     Name of file or path to gtf file
    result  Name of file or path to file containing filtered reads that align to protein coding genes
'''

args = docopt(usage)

# Open GTF and create database for gene access
gtf = gffutils.create_db('<gtf>', dbfn = "genes.db", force=True, keep_order=True)

# Open input file for read access and result file for result storage
input = pysam.AlignmentFile('<input>', "rb")
result = pysam.AlignmentFile('<result>', "wb", template=input)
for read in input.fetch():
    region = (read.reference_name, read.query_alignment_start, read.query_alignment_end)
    for feature in gffutils.FeatureDB.region(region, completely_within=False):
        if feature.attributes["gene_biotype"][0] == "protein_coding":
            result.write(read)
            break
input.close()
result.close()


