import csv


def formatMNEEvents(input, output, delimiter):
    rows = []
    with open(input, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)

    with open(output, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=' ')
        writer.writerows(rows)
    print(f'{output} done.')


def writeFile(filename, rows):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=' ')
        writer.writerows(rows)
