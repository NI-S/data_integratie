"""

this script reads CSV files of clinical data and maps it to SNOMED terms

functions:

    * main - the main function of the script
    *postgre_connect - connects & disconnects with database
    *readcsv - reads input csv files and converts it to output files
    *find_value - converts input term to standard SNOMED term
"""

import psycopg2
import csv
import Levenshtein
import glob, os
import re


def readcsv(cur):
    """Reads csv files of patients and returns csv files with standard
    SNOMED terms

    Parameters
    ----------
    cur: cursor
        the cursor used to work with sql

    """
    currentColumn = "DoNotRead"
    #the program only reads columns with an appropriate header
    os.chdir("./csvfiles2")
    for file in glob.glob("*.csv"):
        with open(file, newline='') as csvfile:
            participantreader = csv.reader(
                csvfile, delimiter=',', quotechar='"')
            writefile = os.path.splitext(file)[0] + "_output.csv"
            with open(writefile, 'w', newline='') as newfile:
                participantwriter = csv.writer(
                    newfile, delimiter=',', quotechar='"')
                for row in participantreader:
                    #values it gives find_value depend on current column
                    #this can be allergy, medical procedure or conditions or symptoms
                    if row[0] == 'Participant':
                        #start of a new column
                        currentColumn = "DoNotRead"
                        #value is reset for new columns
                        if row[1].lower() in \
                                ("conditions or symptom", "immunization"):
                            currentColumn = "conditions or symptom"
                            participantwriter.writerow(row)
                        elif row[1].lower() == "allergy":
                            currentColumn = "allergy"
                            participantwriter.writerow(row)
                        elif row[1].lower() == "medical procedure":
                            currentColumn = "procedure"
                            participantwriter.writerow(row)
                    elif currentColumn == "conditions or symptom":
                        matching_value, exactMatch = \
                            find_value(cur, 'Clinical Finding',
                                       row[1].lower(), False)
                        if (exactMatch):
                            participantwriter.writerow(
                                [row[0], matching_value])
                        else:
                            participantwriter.writerow(
                                [row[0], matching_value, "not exact match"])
                    elif currentColumn == "allergy":
                        matching_value, exactMatch = \
                            find_value(cur, 'Clinical Finding',
                                       row[1].lower(), True)
                        if (exactMatch):
                            participantwriter.writerow(
                                [row[0], matching_value])
                        else:
                            participantwriter.writerow(
                                [row[0], matching_value, "not exact match"])
                    elif currentColumn == "procedure":
                        matching_value, exactMatch = find_value(cur,
                                                                'Procedure',
                                                                row[1].lower(),
                                                                False)
                        if(exactMatch):
                            participantwriter.writerow([row[0],
                                                        matching_value])
                        else:
                            participantwriter.writerow([row[0],
                                                        matching_value,
                                                        "not exact match"])
                            print(matching_value)
def postgre_connect():
    """connects with postgreSQL database, runs readcsv an disconnects

    """
    conn = None
    try:

        print('Connecting ...')
        conn = psycopg2.connect(host='145.74.104.145', port='5432',
                                database='postgres', user='j3_g4',
                                password='Blaat1234')

        cur = conn.cursor()
        readcsv(cur)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def find_value(cur, snomedclass, value, allergy):
    """matches a term to something in the SNOMED index

    Parameters
    ----------
    cur : cursor
        The cursor used to interact with the database
    snomedclass : str
        concept class
    value: str
        value to map to standard snomed term
    alelrgy: bool
        whether or not the current column is "allergy"

    Returns
    -------
    found_row: str
        the standard SNOMED term
    exactMatch: bool
        whether or not an exact match could be found
    """
    exactMatch = True
    match_found = False
    if allergy:
        cur.execute(
            "SELECT concept_name, "
            "regexp_matches(LOWER(concept_name), %(like)s)  "
            "FROM j3_g4.concept where vocabulary_id = 'SNOMED' "
            "AND standard_concept = 'S' AND concept_class_id = %(snomclass)s "
            ,
            dict(snomclass=snomedclass,
                 like='(^' + value + ' allergy$|^allergy to ' + value + '$)'))
        found_row = str(cur.fetchone()).split(',')[0][1:]
        # simply using cur.fetchone()[0] did not work
        if cur.rowcount == 0:
            #we try to find if any standard terms contain the search term
            exactMatch = False
            cur.execute(
                "SELECT concept_name FROM j3_g4.concept where vocabulary_id = "
                "'SNOMED' AND standard_concept = 'S' "
                "AND concept_class_id = %(snomclass)s "
                "AND LOWER(concept_name) LIKE %(like)s"
                " AND LOWER(concept_name) LIKE %(allergy)s",
                dict(snomclass= snomedclass, like= '%' + value + '%', allergy = '%allergy%'))
            found_row = str(cur.fetchone()).split(',')[0][1:]
            # simply using cur.fetchone()[0] did not work
            if cur.rowcount == 0:
                cur.execute(
                    "SELECT concept_id, concept_name FROM j3_g4.concept "
                    "where vocabulary_id = 'SNOMED' "
                    "AND standard_concept = 'S' "
                    "AND concept_class_id = %(snomclass)s  "
                    "order by length(concept_name) desc",
                    dict(snomclass = snomedclass))
                #this is ordered by length to find the longest standard term
                #that is still wholly contained within the search term
                found_table = cur.fetchall()
                lowest_value = 0
                for row in found_table:
                    if re.match(('.*' +
                                 re.sub('[^a-z\d\s]', '',
                                        row[1].lower()) + '.*'),
                                "allergy to " + value)\
                            or re.match(('.*' + re.sub('[^a-z\d\s]', '',
                                                       row[1].lower()) + '.*'),
                                        value + " allergy"):
                        found_row = row[1]
                        break
                    current_value = Levenshtein.distance("Allergy " + value, row[1])
                    #if nothing better is found, the lowest levenshtein distance is used
                    if current_value < lowest_value or lowest_value == 0:
                        lowest_value = current_value
                        found_row = row[1]
    else:
        cur.execute("SELECT concept_name FROM j3_g4.concept "
                    "where vocabulary_id = 'SNOMED'"
                    " AND standard_concept = 'S' AND concept_class_id = %s "
                    "AND LOWER(concept_name) = %s", (snomedclass, value))
        found_row = str(cur.fetchone()).split(',')[0][1:]
        # simply using cur.fetchone()[0] did not work
        if cur.rowcount > 0:
            match_found = True
        else:
            # we try to find if any standard terms contain the search term
            exactMatch = False
            cur.execute(
                "SELECT concept_name, regexp_matches(LOWER(concept_name), "
                "%(like)s) FROM j3_g4.concept where vocabulary_id = "
                "'SNOMED' AND standard_concept = 'S' "
                "AND concept_class_id = %(snomclass)s "
                , dict(snomclass=snomedclass,
                       like= '(^| )' + value + '($| )'))
            found_row = str(cur.fetchone()).split(',')[0][1:]
            # simply using cur.fetchone()[0] did not work
            if cur.rowcount > 0:
                match_found = True
            else:
                cur.execute(
                    "SELECT concept_id, concept_name FROM j3_g4.concept "
                    "where vocabulary_id = 'SNOMED'"
                    " AND standard_concept = 'S' "
                    "AND concept_class_id = %(snomclass)s  "
                    "order by length(concept_name) desc",
                    dict(snomclass= snomedclass))
                #this is ordered by length to find the longest standard term
                #that is still wholly contained within the search term
                found_table = cur.fetchall()
                lowest_value = 0
                for row in found_table:
                    if re.match(('.*' +
                                 re.sub('[^a-z\d\s]', '',
                                        row[1].lower()) + '.*'), value):
                        found_row = row[1]
                        match_found = True
                        break
                    current_value = Levenshtein.distance(value, row[1])
                    #if nothing better is found, the lowest levenshtein distance is used
                    if current_value < lowest_value or lowest_value == 0:
                        lowest_value = current_value
                        found_row = row[1]
            if match_found == False:
                print(value)

                cur.execute(
                    "SELECT A.concept_id, regexp_matches(LOWER(A.concept_synonym_name),"
                    " %(like)s) FROM j3_g4.concept_synonym A"
                    " WHERE A.concept_id in (SELECT B.concept_id "
                    " FROM j3_g4.concept B "
                            "where B.vocabulary_id = 'SNOMED'"
                            " AND B.standard_concept = 'S' "
                            "AND B.concept_class_id = %(snomclass)s  )"
                    "AND A.language_concept_id = '4180186' "
                    "order by length(A.concept_synonym_name) desc",
                    dict(like='(^| )' + value + '($| )',
                         snomclass=snomedclass))
                #look for matching synonyms
                if cur.rowcount > 0:
                    found_table = cur.fetchall()
                    for row in found_table:
                        cur.execute(
                            "SELECT concept_id, concept_name FROM j3_g4.concept "
                            "where vocabulary_id = 'SNOMED'"
                            " AND standard_concept = 'S' "
                            "AND concept_class_id = %(snomclass)s  "
                            "AND concept_id = %(id)s"
                            "order by length(concept_name) desc",
                            dict(snomclass=snomedclass,
                                 id=row[0]))
                        if cur.rowcount >0:
                            match_found = True
                            found_row = str(cur.fetchone()).split(',')[1][1:]
                            break
            if match_found == False:
                print("no match")
                cur.execute(
                    "SELECT concept_id, concept_synonym_name FROM j3_g4.concept_synonym A "
                    " WHERE A.concept_id in (SELECT B.concept_id "
                    " FROM j3_g4.concept B "
                            "where B.vocabulary_id = 'SNOMED'"
                            " AND B.standard_concept = 'S' "
                            "AND B.concept_class_id = %(snomclass)s  )"
                    "AND A.language_concept_id = '4180186' "
                    "order by length(concept_synonym_name) desc",
                dict(snomclass=snomedclass))
                # this is ordered by length to find the longest standard term
                # that is still wholly contained within the search term
                found_table = cur.fetchall()
                for row in found_table:
                    if re.match(('.*' +
                                 re.sub('[^a-z\d\s]', '',
                                        row[1].lower()) + '.*'), value):
                        found_row = row[1]
                        break
                    current_value = Levenshtein.distance(value, row[1])
                    # if nothing better is found, the lowest levenshtein distance is used
                    if current_value < lowest_value or lowest_value == 0:
                        cur.execute(
                            "SELECT concept_id, concept_name FROM j3_g4.concept "
                            "where vocabulary_id = 'SNOMED'"
                            " AND standard_concept = 'S' "
                            "AND concept_class_id = %(snomclass)s  "
                            "AND concept_id = %(id)s"
                            "order by length(concept_name) desc",
                            dict(snomclass=snomedclass,
                                 id=row[0]))
                        if cur.rowcount > 0:
                            lowest_value = current_value
                            found_row = str(cur.fetchone()).split(',')[1][1:]

    return found_row, exactMatch

if __name__ == '__main__':
    postgre_connect()

