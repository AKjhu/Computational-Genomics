import pysam
import sys
import gffutils

# Open transcriptome file for reading
#transcriptome = pysam.AlignmentFile("/home/sunnyk/GenomicsFiles/reads.1.sanitize.noribo.toTranscriptome.sorted.bam", "rb")

# Create dictionary and store all query names from transcriptome file into dictionary as keys with value 0
#t_qname = {}
#for x in transcriptome:
 #   query = x.query_name
  #  t_qname[query] = 0
#transcriptome.close()

# Open GTF and create a dictionary with the starting positions of all protein coding genes as keys and
# ending positions as values
#gtf_db = gffutils.create_db("/home/sunnyk/GenomicsFiles/genes.gtf", dbfn="genes.db", force=True, keep_order=True)

gtf = gffutils.FeatureDB("genes.db", keep_order=True)
coding_genes = {}
all_features = gtf.all_features()
for i in range(len(all_features) - 1):
    gene = all_features[i]
    if gene.attributes["gene_biotype"][0] == "protein_coding":
        if
        print(gene.attributes["gene_biotype"][0])

gtf_ranges = {}

# Check each genome query name to verify if it is in the transcriptome; if not found, write read to output file
#genome = pysam.AlignmentFile("/home/sunnyk/GenomicsFiles/reads.1.sanitize.noribo.toGenome.sorted.bam", "rb")
#result = pysam.AlignmentFile("/home/sunnyk/GenomicsFiles/results.bam", "wb", template=genome)
#for read in genome:
#   if read.query_name not in t_qname:
  #      result.write(read)

#genome.close()
#result.close()
