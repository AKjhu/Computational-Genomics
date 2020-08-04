import pysam
import sys

# Open genome file for reading
transcriptome = pysam.AlignmentFile("/home/sunnyk/GenomicsFiles/reads.1.sanitize.noribo.toTranscriptome.sorted.bam", "rb")
#genome = pysam.AlignmentFile("/home/sunnyk/GenomicsFiles/reads.1.sanitize.noribo.toGenome.sorted.bam", "rb")
#result = pysam.AlignmentFile("/home/sunnyk/GenomicsFiles/results.bam", "wb", template=genome)

# Create dicctionary and store all query names from genome file into dictionary as keys with value 0
t_qname = {}
for x in transcriptome:
    query = x.query_name
    t_qname[query] = 0
transcriptome.close()

# Check each genome query name to verify if it is in the transcriptome; if found, increase its value to 1
genome = pysam.AlignmentFile("/home/sunnyk/GenomicsFiles/reads.1.sanitize.noribo.toGenome.sorted.bam", "rb")
result = pysam.AlignmentFile("/home/sunnyk/GenomicsFiles/results.bam", "wb", template=genome)
for read in genome:
    for key in t_qname:
        if read.query_name == key:
            #result.write(read)
            # g_qname[key] += 1
            break
    result.write(read)
# transcriptome.close()

# Loop through dictionary and create new bam file containing reads not found in transcriptome
# result = pysam.AlignmentFile("/home/sunnyk/GenomisFiles/results.bam", "wb", template=genome)
# for read in genome:
  #  if g_qname[read.query_name] == 0:
   #     result.write(read)


genome.close()
result.close()