from database import Database_connection
from person_table import *

def main():
    dicts = create_dicts()
    for i in range(len(dicts)):
        index = i + 1
        if index % 2 != 0:      #   Value is not even
            insert_db("person", dicts[i])
            pass
        else:
            insert_db("procedure_occurrence", dicts[i])      # Value is even
    get_data_db()


def create_dicts():
    dicts = []
    files = ["PGPC-4.csv", "PGPC-14.csv", "PGPC-38.csv"]
    for file in files:
        for i in ["person","procedure"]:
            synonym = create_synonym(i)
            content = open_file(file)
            dict_patient, tmp_list = add_to_dict(content, synonym)
            dict_patient = add_values_to_dict(dict_patient, tmp_list)
            dict_patient = check_for_not_null(dict_patient, i,files.index(file))

            dict_patient = change_string_to_int(dict_patient)
            dicts.append(dict_patient)
    return dicts


def insert_db(table_name,dict_patient):
    table_name = table_name
    keys = ", ".join(dict_patient.keys())
    values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in dict_patient.values())
    Database = Database_connection()
    Database.postgre_connect()
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table_name, keys,values)
    Database.postgre_excute_query(sql)
    print("done")
    Database.postgre_discconnect()

def get_data_db():
    Database = Database_connection()
    Database.postgre_connect()
    sql = "SELECT * from PERSON"
    Database.postgre_excute_query(sql)
    Database.postgre_fetch_results()
    Database.postgre_discconnect()

main()