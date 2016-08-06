import sqlite3
from bs4 import BeautifulSoup
import requests
import re
import time
import sys, getopt
from random import uniform
import urllib.request
import json
import pprint as pp

#always use console encoding
enc = sys.stdout.encoding

# Function for reading command line arguments
def processArguments(argv):
    # Get optcodes and input from cammand line arguments
    opts, args = getopt.getopt(argv,"i:o:",["idb=","odb="])
    indb = ""
    outdb = ""
    for opt, arg in opts:
        if opt in ("-i", "--idb"):
            indb = arg
        elif opt in ("-o", "--odb"):
            outdb = arg
    if outdb == "":# or indb == "":
        # <inputdb> - name of the input db file
        # <outputdb> - name of the output db file
        print ("Please use: python searchApps.py -i <inputdb> -o <outputdb>")
    else:
        findRatings(outdb, indb)

# Reads term from terms.db, searchs play store,
# adds resulting IDs to queue.db
def findRatings(outdb, indb=""):
    print("STARTING APP SEARCH, PLEASE WAIT")
    # indb.db
    if indb != "":
	    indb = sqlite3.connect(indb)
	    ic = indb.cursor()
	    ic.execute('''SELECT * FROM games''')
    # test.db
    db = sqlite3.connect(outdb)
    c = db.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS games
        (game_id INT PRIMARY KEY,
        name TEXT,
        type TEXT,
        required_age INT,
        num_dlc INT,
        detailed_description TEXT,
        about_the_game TEXT,
        supported_languages TEXT,
        header_image TEXT,
        website TEXT,
        min_req TEXT,
        rec_req TEXT,
        developers TEXT,
        publishers TEXT,
        demo_id INT,
        platflorms TEXT,
        metacritic INT,
        metaurl TEXT,
        release_date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS categories
        (game_id INT PRIMARY KEY,
        id INT,
        description TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS genres
        (game_id INT PRIMARY KEY,
        id INT,
        description TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS screenshots
        (game_id INT PRIMARY KEY,
        id INT,
        path_thumbnail TEXT,
        path_full TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS movies
        (game_id INT PRIMARY KEY,
        id INT,
        name TEXT,
        thumbnail TEXT,
        webm480 TEXT,
        webm TEXT)''')
    db.commit()
    steamurl = 'http://api.steampowered.com/'
    module = 'ISteamApps/GetAppList/v0001/'

    with urllib.request.urlopen(steamurl + module) as r:
    	data = json.loads(r.read().decode(enc))
    	data = data['applist']['apps']['app']
    	count = 0
    	for game in data:
    		appid = game['appid']
    		appurl = 'http://store.steampowered.com/api/appdetails?appids=' + str(appid)
    		with urllib.request.urlopen(appurl) as r2:
    			d = json.loads(r2.read().decode(enc))
    			success = d[str(appid)]['success']
    			if success:
    				d = d[str(appid)]['data']
	    			values = (d['steam_appid'], d['name'], d['type'], d['required_age'],
	    				len(d['dlc']) if d.get('dlc') else 0, d['detailed_description'], d['about_the_game'], check_exist(d, 'supported_languages'),
	    				d['header_image'], d['website'], check_exist_list(d['pc_requirements'], 'minimum'), check_exist_list(d['pc_requirements'], 'recommended'),
	    				','.join(check_exist(d, 'developers')), ','.join(check_exist(d, 'publishers')), 0, ''.join(['1' if d['platforms'][x] else '0' for x in d['platforms']]),
	    				int(d['metacritic']['score']) if d.get('metacritic') else 0, check_exist(d['metacritic'], 'url') if d.get('metacritic') else '',
	    				d['release_date']['date'])
	    			c.execute('''INSERT OR IGNORE INTO games VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', values)
	    			if d.get('categories'):
	    				for cat in d['categories']:
	    					values = (d['steam_appid'], cat['id'], cat['description'])
	    					c.execute('''INSERT OR IGNORE INTO categories VALUES(?,?,?)''', values)
	    			if d.get('genres'):
	    				for cat in d['genres']:
	    					values = (d['steam_appid'], cat['id'], cat['description'])
	    					c.execute('''INSERT OR IGNORE INTO genres VALUES(?,?,?)''', values)
	    			if d.get('screenshots'):
	    				for cat in d['screenshots']:
	    					values = (d['steam_appid'], cat['id'], cat['path_thumbnail'], cat['path_full'])
	    					c.execute('''INSERT OR IGNORE INTO screenshots VALUES(?,?,?,?)''', values)
	    			if d.get('movies'):
	    				for cat in d['movies']:
	    					values = (d['steam_appid'], cat['id'], cat['name'], cat['thumbnail'], check_exist(cat['webm'], '480'), check_exist(cat['webm'], 'max'))
	    					c.execute('''INSERT OR IGNORE INTO movies VALUES(?,?,?,?,?,?)''', values)
	    			db.commit()
    		print('ADDED GAME ' + game['name'])
    		time.sleep(1)

def check_exist_list(a, b):
	if not isinstance(a, list):
		return a[b] if a.get(b) else ''
	else:
		return ''

def check_exist(a, b):
	return a[b] if a.get(b) else ''

if __name__ == "__main__":
    processArguments(sys.argv[1:])