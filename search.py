import sqlite3
import sys, getopt

from init_game_db import init_game_db
from search_games import add_from_db, add_from_steam

#always use console encoding
enc = sys.stdout.encoding

# Function for reading command line arguments
def processArguments(argv):
    # Get optcodes and input from cammand line arguments
    opts, args = getopt.getopt(argv,"i:o:g:t:",["indb=","outdb=","gamesdb=","type="])
    in_db = ""
    out_db = ""
    games_db = ""
    stype = ""
    for opt, arg in opts:
        if opt in ("-i", "--indb"):
            in_db = arg
        elif opt in ("-o", "--outdb"):
            out_db = arg
        elif opt in ("-g", "--gamesdb"):
            games_db = arg
        elif opt in ("-t", "--type"):
            stype = arg
    if stype == "" or out_db == "":# or in_db == "":
        # <type> - type of search (games, images, etc)
        # <inputdb> - name of the input db file
        # <outputdb> - name of the output db file
        print ("Please use: python search.py -t <type> -i <inputdb> -o <outputdb>")
    else:
        return (stype, (out_db, in_db, games_db))

# Reads term from games.db,
# adds resulting IDs to test.db
def findGames(out_db, in_db="", games_db=""):
    out_db = sqlite3.connect(out_db)
    init_game_db(out_db)
    if in_db == "":
        games_db = sqlite3.connect(games_db)
        add_from_steam(out_db, games_db)
    else:
        in_db = sqlite3.connect(in_db)
        add_from_db(in_db, out_db)

if __name__ == "__main__":
    args = processArguments(sys.argv[1:])
    if args != None:
        stype, args = args
        if stype == "games":
            findGames(*args)
