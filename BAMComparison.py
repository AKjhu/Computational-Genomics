import pysam
import sys

# Open genome file for reading
#transcriptome = pysam.AlignmentFile("/home/sunnyk/GenomicsFiles/reads.1.sanitize.noribo.toTranscriptome.sorted.bam", "rb")
genome = pysam.AlignmentFile("/home/sunnyk/GenomicsFiles/reads.1.sanitize.noribo.toGenome.sorted.bam", "rb")
result = pysam.AlignmentFile("/home/sunnyk/GenomicsFiles/results.bam", "wb", template=genome)

# Create dicctionary and store all query names from genome file into dictionary as keys with value 0
g_qname = {}
for x in genome:
    query = x.query_name
    g_qname[query] = 0

# Check each genome query name to verify if it is in the transcriptome; if found, increase its value to 1
transcriptome = pysam.AlignmentFile("/home/sunnyk/GenomicsFiles/reads.1.sanitize.noribo.toTranscriptome.sorted.bam", "rb")
for key in g_qname:
    for read in transcriptome:
        if key == read.query_name:
            g_qname[key] += 1
            break
transcriptome.close()

# Loop through dictionary and create new bam file containing reads not found in transcriptome
result = pysam.AlignmentFile("/home/sunnyk/GenomisFiles/results.bam", "wb", template=genome)
for read in genome:
    if g_qname[read.query_name] == 0:
        result.write(read)


genome.close()
result.close()
