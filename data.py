import csv

examples = []

with open("examples.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        if row['text'] == row['correction']:
            row['correction'] = "No corrections required."
        examples.append(row)
