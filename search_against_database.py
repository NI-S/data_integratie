import sys
import psycopg2


def search_db(term):
    """
    searches against databse in the table "concept" with colums "concept_name and concept_id"
    term wil be schearcd in concept collum
    :param term: term that wil be searched in the concept_name colum
    :return: the furst result found in db
    """
    conn = psycopg2.connect(host='145.74.104.145', port='5432',
                            database='postgres', user='j3_g4',
                            password='Blaat1234')
    cur = conn.cursor()

    cur.execute(
        f"SELECT concept_name, concept_id "
        f"FROM j3_g4.concept "
        f"where (vocabulary_id = 'HGNC' OR vocabulary_id ='OMOP Exstension')"
        f"AND standard_concept = 'S' AND concept_name LIKE '{term}%'")

    result = cur.fetchall()
    cur.close()
    return result


if __name__ == "__main__":
    """ maps al gene names from data/{nummer}/pgp_data/PGPC_00{nummer}_chr21_filtered_10.vcf to convential names from 
    the provided db.
    Example to run file via command line: python3 search_against_database.py {vcf_File}
    """
    vcf_name = sys.argv[1]
    vcf_maped = sys.argv[2]

    with open(vcf_name) as vcf, open(vcf_maped, "w+") as vcf_maped :
        for line in vcf:
            if not line.startswith('#'):
                info = line.split("\t")[7].split("|")
                gene = info[3]
                id = "none"
                naam = "none"
                try:
                    id = search_db(gene)[0][1]
                    naam = search_db(gene)[0][0]
                except: pass
                vcf_maped.write(f"{id}, {naam}\n")
