import pysam
import gffutils
import docopt

usage = '''
Genome Transcriptome File Comparator

Usage:
    BAMComparison.py <genome> <transcriptome> <result>
    BAMComparison.py -h | --help
    
Arguments:
    genome  Name of file or path to file containing genome reads
    transcriptome   Name of file or path to file containing transcriptome reads
    result  Name of file or path to new file containing reads found in genome but not in transcriptome
'''

args = docopt(usage)

# Open transcriptome file for reading
transcriptome = pysam.AlignmentFile('<transcriptome>', "rb")

# Create dictionary and store all query names from transcriptome file into dictionary as keys with value 0
t_qname = {}
for x in transcriptome:
    query = x.query_name
    t_qname[query] = 0
transcriptome.close()


# Check each genome query name to verify if it is in the transcriptome; if not found, write read to output file
genome = pysam.AlignmentFile('<genome>', "rb")
result = pysam.AlignmentFile('<result>', "wb", template=genome)
for read in genome:
   if read.query_name not in t_qname:
        result.write(read)

genome.close()
result.close()



