from collections import OrderedDict

def main():
    synonym = create_synonym()
    content = open_file("PGPC-4.csv")
    dict_patient_4, tmp_list = add_to_dict(content, synonym)
    dict_patient_4 = add_values_to_dict(dict_patient_4, tmp_list)
    dict_patient_4 = check_for_not_null(dict_patient_4)
    dict_patient_4 = change_string_to_int(dict_patient_4)
    print(dict_patient_4)


def create_synonym():
    synonym = {"Participant": "person_id", "Sex": "gender_concept_id", "Birth year": "year_of_birth",
    "Birth month": "month_of_birth", "Birth day": "day_of_birth", "Birth date": "birth_datetime",
    "Race": "race_concept_id", "Ethnicity": "ethnicity_concept_id",}
    return synonym


def open_file(file):
    with open(file, 'r') as patient_4:
        content = patient_4.read()
    content = content.split('\n')
    return content

def add_to_dict(content, synonym):
    count = 0; dict_patient_4 = {}; tmp_list = []
    for element in content:
        count += 1
        element = element.split(",")

        # Add keys to dictionary, happens when the count is odd
        if count % 2 != 0:

            for i in range(len(element)):
                for k,v in synonym.items():
                    if k == element[i]:
                        dict_patient_4[synonym[k]] = ""

        # Add values to existing keys, happens when the count is even
        else:
            for i in range(len(element)):
                tmp_list.append(element[i])

    return(dict_patient_4, tmp_list)

def add_values_to_dict(dict_patient_4, tmp_list):
    count = 0
    for k, v in dict_patient_4.items():

        dict_patient_4[k] = tmp_list[count]
        count += 1
    return dict_patient_4

def check_for_not_null(dict_patient_4):

    mandatory_keys = ["person_id", "gender_concept_id", "year_of_birth", "race_concept_id", "ethnicity_concept_id"]
    for k in mandatory_keys:
        if dict_patient_4.get(k) is None:
            if k == "person_id":
                dict_patient_4[k] = ""
            else:
                dict_patient_4[k] = 0
    return dict_patient_4

def change_string_to_int(dict_patient_4):
    for k,v in dict_patient_4.items():
        if k == "person_id":
            sep = "-"
            number = dict_patient_4[k].split(sep, 1)[1]
            dict_patient_4[k] = number
        if k == "gender_concept_id":
            if dict_patient_4[k] == "M":
                dict_patient_4[k] = 8507
            else:
                dict_patient_4[k] = 8532
        if k == "ethnicity_concept_id":
            if dict_patient_4[k] == "Hispanic":
                dict_patient_4[k] = 38003563        # Found on athena
            else:
                dict_patient_4[k] = 38003564        # Found on athena
    return dict_patient_4



main()