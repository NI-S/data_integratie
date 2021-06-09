"""Noah Scheffer

Call the functions and insert the results from the dictionaries to the database.
To see if it is inserted correctly it is also possible to retrieve the data.
Last time updated: 09-06-2021
"""

from database import Database_connection
from generate_dicts import *
import os, glob

def main():
    dicts = create_dicts()
    dicts = create_dicts_measurement(dicts)
    for i in range(len(dicts)):
        index = i + 1
        if index % 2 != 0 and index < 7:      #   Value is not even
            insert_db("person", dicts[i])
            pass
        elif index < 7:
            insert_db("procedure_occurrence", dicts[i])      # Value is even
            pass
        else:
            pass
            insert_db("measurement", dicts[i])      # Contains all the measurement data
    #get_data_db("person")


def create_dicts():
    """Iterate over the files.
    create the synonym list which is used to search words in the file.
    Read the file and add content of file to dictionary and temporary list.
    Add the values from the temporary list to the keys in the dictionary.
    Check if keys contain a empty value if so, add a value.
    Change the values of some keys if necessary.
    Add the made dict to the dicts list.
    :return:list containing dictionaries.
    """
    dicts = []
    files = ["data/csv/PGPC-04.csv", "data/csv/PGPC-14.csv", "data/csv/PGPC-38.csv"]

    for file in files:
        for i in ["person","procedure"]:
            synonym = create_synonym(i)
            content = open_file(file)
            dict_patient, tmp_list = add_to_dict(content, synonym)
            dict_patient = add_values_to_dict(dict_patient, tmp_list)
            dict_patient = check_for_not_null(dict_patient, i,files.index(file), None, None, None)
            dict_patient = change_string_to_int(dict_patient)
            dicts.append(dict_patient)
    return dicts

def create_dicts_measurement(dicts):
    """Iterate over the files.
    Open file and get the concept and date. Loop over the concepts.
    Add to the dictionary while looping over the concepts.
    Add the new dictionary to the existing dicts list.
    :param: dicts: list to which the dictionaries wil be added.
    :return:list containing dictionaries.
    """
    vcf_files = ["data/04/pgp_data/PGPC_0004_chr21_filtered.vcf", "data/14/pgp_data/PGPC_0014_chr21_filtered.vcf",
                 "data/38/pgp_data/PGPC_0038_chr21_filtered.vcf"]
    variant_files = ["data/04/pgp_data/genes_mapped04.csv", "data/14/pgp_data/genes_mapped14.csv", "data/38/pgp_data/genes_mapped38.csv"]
    count = 1
    for file in variant_files:
        id = get_person_id(file)
        content = open_file(file)
        concept = get_measurement_concept(content)
        date = get_date(vcf_files[0])
        for c in concept:
            dict_patient = {}
            dict_patient = check_for_not_null(dict_patient, "measurement", c, date, id, count)
            dict_patient = change_string_to_int(dict_patient)
            dicts.append(dict_patient)
            count = count + 1
        count += 10
    return dicts


def insert_db(table_name,dict_patient):
    """Seperate the content of the dictionaries in keys and values.
    Use the table_name to specify the tablename.
    Connect with the database and insert using the tablename and the keys and values of the dictionary.
    Disconnect with the database when done.
    :param table_name:table_name which u want to insert to.
    :param dict_patient:the dictionary which is used to insert data to the database.
    :return: Nothing
    """
    table_name = table_name
    keys = ", ".join(dict_patient.keys())
    values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in dict_patient.values())
    Database = Database_connection()
    Database.postgre_connect()
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table_name, keys,values)
    Database.postgre_excute_query(sql)
    print("done")
    Database.postgre_discconnect()


def get_data_db(table_name):
    """Connect to database and execute the sql query.
    :param sql: Used to select which table you want the entries from.
    :return: Nothing
    """
    Database = Database_connection()
    Database.postgre_connect()
    sql = "SELECT * from (%s)" % (table_name)
    Database.postgre_excute_query(sql)
    Database.postgre_fetch_results()
    Database.postgre_discconnect()

main()