import pysam
import gffutils
from docopt import docopt

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

# Open GTF and create a dictionary with the starting positions of all protein coding genes as keys and
# ending positions as values
#gtf_db = gffutils.create_db("/home/sunnyk/GenomicsFiles/genes.gtf", dbfn="genes.db", force=True, keep_order=True)

gtf = gffutils.FeatureDB("genes.db", keep_order=True)
# coding_genes = {}
regions = {}
# Takes entire gtf into memory
all_features = gtf.all_features()
while i < len(all_features):
    gene = all_features[i]
    if gene.attributes["gene_biotype"][0] == "protein_coding":
        j = i + 1
        region = (gene.seqid, gene.start, gene.end)
        while j < len(all_features) and all_features[j].ID == gene.ID:
            if all_features[j].end > region[2]:
                region[2] = all_features[j].end
            j += 1
        regions[region] = 0
    i = j + 1
        #print(gene.attributes["gene_biotype"][0])


# Check each genome query name to verify if it is in the transcriptome; if not found, write read to output file
genome = pysam.AlignmentFile('<genome>', "rb")
result = pysam.AlignmentFile('<result>', "wb", template=genome)
for read in genome:
   if read.query_name not in t_qname:
        result.write(read)

genome.close()
result.close()
p_coding = {}
result = pysam.AlignmentFile('<result>', "rb")
for region in regions:
    for read in results.fetch(region[0], region[1], region[2]):
        p_coding[read] = 0


