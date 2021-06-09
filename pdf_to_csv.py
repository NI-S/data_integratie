import tabula
import sys

if __name__ == "__main__":
    """ Converts pdf to csv using tabula, all pages are converted to one csv.
    Example to run file via command line: python3 pfg_to_csv.py {pdf input}
    Multiple pdf can be converted ad once, simply add them behind the first input in the command above.
    """
    arg = sys.argv
    for i in range(1, len(arg)):
        pdf = arg[i]
        new_csv = ("data/csv/" + arg[i].split("/")[-1].split(".")[0] + ".csv")
        file = open(new_csv, "w+")
        file.close()
        print(pdf, "->", new_csv)
        tabula.convert_into(pdf, new_csv, output_format="csv", pages="all")
