import sqlite3
import csv

con = sqlite3.connect('mymdb.db')
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS titles (
	id STRING PRIMARY KEY,
   	type STRING,
	primary_title STRING,
    original_title STRING,
    is_adult BOOLEAN,
    start_year INTEGER,
    end_year INTEGER,
    runtime_minutes INTEGER,
    genres STRING,
    average_rating FLOAT,
    num_votes INTEGER
    );""")

con.commit()

with open('data/title.basics.tsv') as datafile:
    data = csv.reader(datafile, delimiter="\t", quotechar=None)
    
    for row in data:
        clean_row = [None if item == r'\N' else item for item in row]
        try: 
            cur.execute("""INSERT INTO titles(id, type, primary_title, original_title, is_adult, start_year, end_year, runtime_minutes, genres)
                VALUES (?,?,?,?,?,?,?,?,?);""", clean_row)
        except:
            print(row)

con.commit()

with open('data/title.ratings.tsv') as datafile:
    data = csv.reader(datafile, delimiter="\t", quotechar=None)
    
    for row in data:
        clean_row = [None if item == r'\N' else item for item in row]
        cur.execute("""UPDATE titles
                SET average_rating = ?, num_votes = ?
                WHERE id = ?;""", [row[1], row[2], row[0]])

con.commit()

con.close()

