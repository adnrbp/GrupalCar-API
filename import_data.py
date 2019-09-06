import csv

def import_csv(csv_filename):
    with open(csv_filename, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pool = Pool(**row)
            pool.save()
            print(pool.name)

