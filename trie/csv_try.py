import csv
with open('scraped.csv') as csv_file:
    spam_reader = csv.DictReader(csv_file)
    i =14
    for raw in spam_reader:
        print(raw['content'])
        i-=1
        if i <0:
            break
