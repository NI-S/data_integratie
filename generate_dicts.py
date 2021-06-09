"""Noah Scheffer

This file is used to create the dicts for the person and procedure_occurence table.
It makes a list with synonyms which is used to find words in the file.
The file is read.
Words from the synonym are add to a dictionary.
The values are add to a list.
Then the values are added to the dictionary.
The values of the dictionary are checked if they are empty.
If they are and are mandatory for the database it gets filled.
The last function replaces some values.
Last time updated: 09-06-2021
"""

from dateutil import parser
import re

def create_synonym(table):
    """Based on what table it is, determine which synonym dictionary must be used.
    :param table:Used to determine which synonym list must be used.
    :return:the dictionary to be used.
    """
    synonym = ""
    if table == "person":
        synonym = {"Participant": "person_id", "Sex": "gender_concept_id", "Birth year": "year_of_birth",
        "Birth month": "month_of_birth", "Birth day": "day_of_birth", "Birth date": "birth_datetime",
        "Race": "race_concept_id", "Ethnicity": "ethnicity_concept_id"}
    elif table == "procedure":
        synonym = {"Procedure": "procedure_occurrence_id", "Participant": "person_id",
                   "Immunization": "procedure_concept_id",
                   "Date": "procedure_date", "Type": "procedure_type_concept_id"}
    return synonym


def open_file(file):
    """Read the file and split it contents on the enter.
    :param file: Used for reading.
    :return:Content of the file.
    """
    with open(file, 'r') as patient:
        content = patient.read()
    content = content.split('\n')
    return content


def get_person_id(file):
    """Get the person_id based on the filename
    :param file: Used to get the person_id
    :return: the person_id
    """
    person_id = int(re.search(r'\d+', file).group())
    return person_id


def get_measurement_concept(content):
    """Get a list with all the concepts.
    Split the text and get the concepts.
    Put the concepts in a list.
    :param content: Used to get the concepts from.
    :return: List with concepts.
    """
    concept = []
    for i in content:
        i = i.split(',')
        concept.append(i[0])
    return concept


def add_to_dict(content, synonym):
    """Declare variables.
    Iterate over the list which contains the content of the file.
    For every entry in the list add one to the variable count.
    If count is odd, add keys to the dictionary.
    If the count is even add it to the tmp_list.
    :param content: Used to check if it contains certain words.
    :param synonym: Used to check if the words is found in the file.
    :return: Dictionary and list containing elements which are found in the file.
    """
    count = 0; dict_patient = {}; tmp_list = []
    for element in content:
        count += 1
        element = element.split(",")

        # Add keys to dictionary, happens when the count is odd
        if count % 2 != 0:

            for i in range(len(element)):
                for k,v in synonym.items():
                    if k == element[i]:
                        dict_patient[synonym[k]] = ""
        # Add values to tmp_list, happens when the count is even
        else:
            for i in range(len(element)):
                tmp_list.append(element[i])
    return(dict_patient, tmp_list)


def add_values_to_dict(dict_patient, tmp_list):
    """Iterate over the elements of the directory.
    Add the elements of the list to the dictionary.
    :param dict_patient:Used to add values to the keys.
    :param tmp_list: Contents are used to add to the keys.
    :return:New dictionary.
    """
    count = 0
    for k, v in dict_patient.items():
        dict_patient[k] = tmp_list[count]
        count += 1
    return dict_patient


def get_date(file):
    """Get the date of the file.
    Read the file and get the line with the date.
    Parse the date.
    :param file: Used to look for the date.
    :return: Date.
    """
    date = ""
    READ = True
    with open (file, "r") as content:
        while READ:
            line = content.readline()
            if line.__contains__("startTime"):
                line = line.split("=", )[1]
                line = line.split(" ")
                date = str(line[2]) + " " + line[1] + " " + str(line[4])
                break
    date = parser.parse(date)
    date = str(date)
    date = date.split(" ",)[0]
    return date


def check_for_not_null(dict_patient, table, key, date, person_id, measurement_id):
    """First determine which are the mandatory keys.
    Then iterate over the mandatory keys.
    Check if the key in the dictionary and is empty.
    If it is empty, add a value.
    :param dict_patient:Used to iterate over it.
    :param table:
    :param key:
    :return:
    """
    if table == "person":
        mandatory_keys = ["person_id", "gender_concept_id", "year_of_birth", "race_concept_id", "ethnicity_concept_id"]
    elif table == "measurement":
        mandatory_keys = ["measurement_id", "person_id", "measurement_concept_id", "measurement_date", "measurement_type_concept_id"]
    else:
        mandatory_keys = ["procedure_occurrence_id", "person_id", "procedure_concept_id", "procedure_date", "procedure_type_concept_id"]
    for k in mandatory_keys:
        if dict_patient.get(k) is None:
            if k == "person_id" and table == "measurement":
                dict_patient[k] = person_id
            elif k == "procedure_occurrence_id":
                dict_patient[k] = key
            elif k == "procedure_date":
                dict_patient[k] = "0001-01-01"
            elif k == "measurement_id":
                dict_patient[k] = measurement_id
            elif k == "measurement_concept_id":
                dict_patient[k] = key
            elif k == "measurement_date":
                dict_patient[k] = date
            else:
                dict_patient[k] = 0
    return dict_patient


def change_string_to_int(dict_patient):
    """Change values to ints.
    :param dict_patient:The dictionary to be checked.
    :return:Dictionary with ints as values.
    """
    for k,v in dict_patient.items():
        if k == "person_id":
            sep = "-"
            try:
                number = dict_patient[k].split(sep, 1)[1]
                dict_patient[k] = number
            except:
                pass
        if k == "gender_concept_id":
            if dict_patient[k] == "M":
                dict_patient[k] = 8507
            else:
                dict_patient[k] = 8532
        if k == "measurement_concept_id":
            if dict_patient[k] == "none":
                dict_patient[k] = 0
        if k == "ethnicity_concept_id":
            if dict_patient[k] == "Hispanic":
                dict_patient[k] = 38003563        # Found on athena
            else:
                dict_patient[k] = 38003564        # Found on athena
    return dict_patient



