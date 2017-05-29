#!python3
import psycopg2
import sys

db = None


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=news")


def getMostPopular3Articles():
    print("\n-----------------------------------------------------------")
    print('Most popular articles of all time:')
    db = connect()
    c = db.cursor()
    c.execute('select * from mostviewedpath;')
    res = c.fetchall()
    db.close()
    for l in res:
        print("\"%s\" -- %s views" % l)
    print("-----------------------------------------------------------\n")


def getMostPopularAuthors():
    print("\n-----------------------------------------------------------")
    print('Most popular authors of all time of all time:')
    db = connect()
    c = db.cursor()
    c.execute('select * from authorviews;')
    res = c.fetchall()
    db.close()
    for l in res:
        print("%s -- %s views" % l)
    print("-----------------------------------------------------------\n")


def getDaysWithMore1PercError():
    print("\n-----------------------------------------------------------")
    print('Days with more than 1% of erros:')
    db = connect()
    c = db.cursor()
    c.execute('select * from errorrequestperc where perc > 1;')
    res = c.fetchall()
    db.close()
    for l in res:
        print("%s -- %s" % (l[0],round(l[1],2)))
    print("-----------------------------------------------------------\n")


def printUsage():
    print('\nUsage: python3 logAnalysis.py [options]\n\n')
    print('python3 logAnalysis.py -a : prints out all logs\n\n')
    print('''python3 logAnalysis.py -getMostPopular3Articles :
    prints out the 3 most popular articles of all time\n\n''')
    print('''python3 logAnalysis.py -getMostPopularAuthors : prints out
    the authors ordered by the sum of view of their articles\n\n''')
    print('''python3 logAnalysis.py -getDaysWithMore1PercError : prints out
    the day where there was more than 1\% of error\n''')
    sys.exit()


def main(argv):
    if len(argv) == 0:
        printUsage()
    elif argv[0] == '-a':
        getMostPopular3Articles()
        getMostPopularAuthors()
        getDaysWithMore1PercError()
    elif argv[0] == '-getMostPopular3Articles':
        getMostPopular3Articles()
    elif argv[0] == '-getMostPopularAuthors':
        getMostPopularAuthors()
    elif argv[0] == '-getDaysWithMore1PercError':
        getDaysWithMore1PercError()


if __name__ == "__main__":
    main(sys.argv[1:])
