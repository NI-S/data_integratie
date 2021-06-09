rule pdf_to_csv:
	input:
		"data/04/pgp-data_pdf/PGPC-4.pdf",
		"data/14/pgp-data_pdf/PGPC-14.pdf",
		"data/38/pgp-data_pdf/PGPC-38.pdf"
	output:
		"data/csv/PGPC-04.csv",
		"data/csv/PGPC-14.csv",
		"data/csv/PGPC-38.csv"
	shell:
		"python3 pdf_to_csv.py {input}"

rule select_chr_21:
    input:
        "data/{nummer}/pgp_data/PGPC_00{nummer}_S1.flt.vcf.gz"

    output:
        "data/{nummer}/pgp_data/PGPC_00{nummer}_chr21.filt.vcf"

    shell:
        "bcftools view {input} --regions chr21 > {output}"

rule add_annotation:
    input:
        "data/{nummer}/pgp_data/PGPC_00{nummer}_chr21.filt.vcf"
    output:
        "data/{nummer}/pgp_data/PGPC_00{nummer}_snpeff_annotate_chr21_flt.vcf"
    shell:
        "java -jar /home/steffen/snpEff/snpEff.jar GRCh37.75 -no-downstream -no-intergenic -no-intron -no-upstream -no-utr  -verbose {input} > {output}"

rule filter_step:
    input:
        "data/{nummer}/pgp_data/PGPC_00{nummer}_snpeff_annotate_chr21_flt.vcf"
    output:
        "data/{nummer}/pgp_data/PGPC_00{nummer}_chr21_filtered.vcf"
    shell:
        """java -jar /home/steffen/snpEff/SnpSift.jar filter "(ANN[*].EFFECT has 'missense_variant' || ANN[*].EFFECT has 'frameshift_variant')" {input} > {output}"""

rule subset_filter:
    input:
        "data/{nummer}/pgp_data/PGPC_00{nummer}_chr21_filtered.vcf"
    output:
        "data/{nummer}/pgp_data/PGPC_00{nummer}_chr21_filtered_10.vcf"
    shell:
        "grep -A 20 CHROM {input} | tail +10 > {output}"

rule map_csv:
    input:
        "data/csv/PGPC-{nummer}.csv"
    output:
        "data/csv/PGPC-{nummer}-mapped.csv"
    shell:
        "mapper.py {input} {output}"

rule fill_database:
    input:
        "data/04/pgp_data/PGPC_0004_chr21_filtered.vcf",
         "data/14/pgp_data/PGPC_0014_chr21_filtered.vcf",
         "data/38/pgp_data/PGPC_0038_chr21_filtered.vcf",
         "data/csv/PGPC-04.csv",
         "data/csv/PGPC-14.csv",
         "data/csv/PGPC-38.csv"
    log:
        "fill_db"
    shell:
        "python3 insert_data.py"

rule mapp_variants:
    input:
        "data/{nummer}/pgp_data/PGPC_00{nummer}_chr21_filtered_10.vcf"
    output:
        "data/{nummer}/pgp_data/genes_mapped{nummer}.csv"
    shell:
        "python3 search_against_database.py {input} {output}"


