from database import Database_connection
from person_table import *

def main():
    for i in ["PGPC-4.csv", "PGPC-14.csv", "PGPC-38.csv"]:
        pass
        #dict_patient = person_dict(i)
        #insert_db(table_name, dict_patient)
    get_data_db()

def person_dict(file):
    synonym = create_synonym()
    content = open_file(file)
    dict_patient, tmp_list = add_to_dict(content, synonym)
    dict_patient = add_values_to_dict(dict_patient, tmp_list)
    dict_patient = check_for_not_null(dict_patient)
    dict_patient = change_string_to_int(dict_patient)
    return dict_patient

def procedure_occurence():


def insert_db(table_name,dict_patient):
    table_name = table_name
    keys = ", ".join(dict_patient.keys())
    values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in dict_patient.values())
    Database = Database_connection()
    Database.postgre_connect()
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table_name, keys,values)
    Database.postgre_excute_query(sql)
    Database.postgre_discconnect()

def get_data_db():
    Database = Database_connection()
    Database.postgre_connect()
    sql = "SELECT * from PERSON"
    Database.postgre_excute_query(sql)
    Database.postgre_fetch_results()
    Database.postgre_discconnect()

main()