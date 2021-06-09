# Data integration

| Teammember | studentnumber |
|------------|:-------------:|
| Noah       | 626290        |
| Steffen    | 616094        |
| Wouter     | 620293        |

## Folders
The folders contain the files that are used for this research.
We examined patients 4,14,38.
The mapper.py is not implemented yet in the insert to database, because of time contraints.


## De python files
### Insert data to database
database.py is a database clas which can be used to connect to the database.

generate_dicts.py creates dictionaries which is used to insert the data in the database.

insert_data.py Call scripts which are mentioned above to fill the generated data by generate_dicts to the database.

* insert_data.py is the script you run * 

## Snakemake file
You need to install snakemake, to run the snakemake file.
In lines 20 and 37 change snp.jar to your snp.jar location.
And change snp.sift to your snp.sift location.

### Running snakemake
To run all scripts type snakemake fill_db.

## Links
The link to the data which needs to be downloaded: https://drive.google.com/drive/folders/1Jnxin0UxVyiVV9ZHqJg1wxjyyYPZ7pPa?usp=sharing
https://docs.google.com/presentation/d/1t1Z0flGtVCUjHXLiy4IJyMAcMUWA8M1W_KF8LxIcOns/edit?usp=sharing link to presentation

