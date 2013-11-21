from argparse import ArgumentParser
import csv, sys



def main():
    parser = ArgumentParser(description = "convert sparkasse-koelnbonn.de .csv files to .qif")
    parser.add_argument("csvfile", help="select sparkasse-koelnbonn.de .csv file")
    args = parser.parse_args()
    csvfile = args.csvfile
    with open(csvfile) as csvfile, open('output.qif', 'w') as qiffile: # infile and outfile as command line arguments
        reader = csv.reader(csvfile, delimiter = ';')
        next(reader) # ignore first csv row
        qiffile.write('!Account\n^\n!Type:Bank\n') # type of file
        for row in reader:
            qiffile.write('D%s\n' % (row[1].replace('.', '/'))) # date field
            qiffile.write('T%s\n' % (row[8].replace(',', '.'))) # amount
            if 'Umsatz gebucht' in row[10]: # check cleared status
                qiffile.write('CR\n') # cleared
            else:
                qiffile.write('C\n') # not cleared
            qiffile.write('P%s\n' % row[5])
            qiffile.write('M%s\n' % row[3])
            qiffile.write('^\n')

if __name__ == '__main__':
    main()
