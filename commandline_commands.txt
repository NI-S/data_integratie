#!/bin/bash

# Used as a template for automating the annotation of the variants
# The files should be replaced with the desired filenames.
# To make a clear distinction between the files, the names ar not changed here.
# Download and install snpeff https://pcingola.github.io/SnpEff/download/


# To install the requirements
sudo apt update
sudo apt install bcftools 
sudo apt install tabix

# Create file which contains only  chromosome 21.
bgzip PGPC_0038_S1.flt.vcf 
tabix -p vcf PGPC_0038_S1.flt.vcf.gz 
bcftools view PGPC_0038_S1.flt.vcf.gz --regions chr21 > PGPC_0038_chr21.filt.vcf

# Annotate the file
java -jar ../snpEff/snpEff.jar GRCh37.75 -no-downstream -no-intergenic -no-intron -no-upstream -no-utr  -verbose PGPC_0038_chr21.filt.vcf > PGPC_0038_snpeff_annotate_chr21_flt.vcf

# Specify which variants can be in the file
java -jar /home/noah/snpEff/SnpSift.jar filter "(ANN[*].EFFECT has 'missense_variant' || ANN[*].EFFECT has 'frameshift_variant')" PGPC_0038_snpeff_annotate_chr21_filt.vcf' > PGPC_0038_chr21_filtered.vcf

# Get only 10 variants
grep -A 10 CHROM PGPC_0038_chr21_filtered.vcf > PGPC_0038_chr21_filtered_10.vcf
