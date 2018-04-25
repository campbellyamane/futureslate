import csv


with open('Pitcher and Hits.csv', 'rb') as inp, open('Pitcher and Hits_edit.csv', 'wb') as out:
    writer = csv.writer(out)
    total_hits = {}
    single = {}
    double = {}
    triple = {}
    hr = {}
    for row in csv.reader(inp):
        if row[0] not in total_hits.keys():
            total_hits[row[0]] = 1
        else:
            total_hits[row[0]] += 1

        if row[1] == '20' and row[0] not in single.keys():
            single[row[0]] = 1
        elif row[1] == '20':
            single[row[0]] += 1

        if row[1] == '21' and row[0] not in double.keys():
            double[row[0]] = 1
        elif row[1] == '21':
            double[row[0]] += 1

        if row[1] == '22' and row[0] not in triple.keys():
            triple[row[0]] = 1
        elif row[1] == '22':
            triple[row[0]] += 1

        if row[1] == '23' and row[0] not in hr.keys():
            hr[row[0]] = 1
        elif row[1] == '23':
            hr[row[0]] += 1
    for p in total_hits.keys():
        try:
            s = float(single[p])/total_hits[p]
        except:
            s = 0
        try:
            d = float(double[p])/total_hits[p]
        except:
            d = 0
        try:
            t = float(triple[p])/total_hits[p]
        except:
            t = 0
        try:
            h = float(hr[p])/total_hits[p]
        except:
            h = 0
        writer.writerow([p, s, d, t, h])
