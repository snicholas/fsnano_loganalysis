#!/usr/bin/env python3
import psycopg2
import sys


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        return psycopg2.connect("dbname=news")
    except:
        print("There was an error connecting to the news database.")
        return None


def executeQuery(query):
    db = connect()
    c = db.cursor()
    c.execute(query)
    res = c.fetchall()
    db.close()
    return res


def getMostPopular3Articles():
    print("\n-----------------------------------------------------------")
    print('Most popular articles of all time:')
    res = executeQuery('select * from mostviewedpath;')
    for l in res:
        print("\"%s\" -- %s views" % l)
    print("-----------------------------------------------------------\n")


def getMostPopularAuthors():
    print("\n-----------------------------------------------------------")
    print('Most popular authors of all time of all time:')
    res = executeQuery('select * from authorviews;')
    for l in res:
        print("%s -- %s views" % l)
    print("-----------------------------------------------------------\n")


def getDaysWithMore1PercError():
    print("\n-----------------------------------------------------------")
    print('Days with more than 1% of errors:')
    res = executeQuery('select * from errorrequestperc where perc > 1;')
    for l in res:
        print("%s -- %s" % (l[0], round(l[1], 2)))
    print("-----------------------------------------------------------\n")


def printUsage():
    print('\nUsage: python3 logAnalysis.py [options]\n\n')
    print('python3 logAnalysis.py -a : prints out all logs\n\n')
    print('''python3 logAnalysis.py -getMostPopular3Articles or -popArt :
    prints out the 3 most popular articles of all time\n\n''')
    print('''python3 logAnalysis.py -getMostPopularAuthors or -popauth : prints out
    the authors ordered by the sum of view of their articles\n\n''')
    print('''python3 logAnalysis.py -getDaysWithMore1PercError or -errdays : prints out
    the day where there was more than 1\% of error\n''')
    sys.exit()


def main(argv):
    if len(argv) == 0:
        printUsage()
    elif argv[0] == '-a':
        getMostPopular3Articles()
        getMostPopularAuthors()
        getDaysWithMore1PercError()
    elif argv[0] == '-getMostPopular3Articles' or argv[0] == '-popart':
        getMostPopular3Articles()
    elif argv[0] == '-getMostPopularAuthors' or argv[0] == '-popauth':
        getMostPopularAuthors()
    elif argv[0] == '-getDaysWithMore1PercError' or argv[0] == '-errdays':
        getDaysWithMore1PercError()


if __name__ == "__main__":
    main(sys.argv[1:])
