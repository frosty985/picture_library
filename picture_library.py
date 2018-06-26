import argparse
from argparse import RawTextHelpFormatter
import os.path
import configparser
import pymysql
from cat import is_face
from exif import imgDetails
from mysql_actions import insert_file


""" Set program arguments """
parser = argparse.ArgumentParser("Process image files and catalog them into a database", formatter_class=RawTextHelpFormatter)
parser.add_argument("image", type=str)
parser.add_argument("-a", "--action", type=str, default="all", help="Action to do:\n" +
                                                                    "(a)ll (default),\n" +
                                                                    "(d)atabase: insert to database,\n" +
                                                                    "fa(c)e: facial regonisation,\n" +
                                                                    "de(t)ect: detect faces for training data, use with -o --out\n"+
                                                                    "(r)efresh: images in the database")
parser.add_argument("-o", "--output", type=str, default="~/piclib", help="Output directory")
parser.add_argument("-c", "--config", type=str, default="config.ini", help="Location of config file")

args = parser.parse_args()
configFileName = args.config

""" Set Golbal varibles """
config = None
con_database = None
con_debug = None
mysqlCur = None


""" Load config file """
if (os.path.exists(configFileName) == False):
    print("\nSorry, the config file " + configFileName + " does not exist\nPlease check the command line, or create a config file")
    exit()
try:
    config = configparser.ConfigParser()
    config.read(configFileName)
    if(len(config.sections()) == 0):
        raise Exception("File", "Empty")
    con_database = config["database"]
    con_debug = config["debug"]
    if con_debug.getboolean("display"):
        show = True
    else:
        show = False

except:
    print("\nError reading config file.\nPlease check it is valid, and try again\n")
    exit()

""" Detect faces for training """
if args.action == "a" or args.action == "all" or args.action == "t" or args.action == "detect":
    img_cat = str(is_face(args.image, debug=True))
    if con_debug.getboolean("message"):
        print("[Debug]\t" + args.image + " is found to be: " + str(img_cat))

""" Insert into database """
if args.action == "a" or args.action == "all" or args.action == "D" or args.action == "database":

    try:
        mysqlConnection = pymysql.connect(host=con_database["host"],
                                          user=con_database["user"],
                                          db=con_database["data"],
                                          passwd=con_database["pass"],
                                          autocommit=True)
        mysqlCur = mysqlConnection.cursor()
    except:
        print("\nThere was an error connecting to the MySQL database.\nPlease check your config file and try again.\n")
        exit()

    if con_debug.getboolean("message"):
        img_details = imgDetails(args.image)
        print("[Debug]\t" + str(img_details))
        print("[Debug]\t Atempting to insert into database")
        insert_file(mysqlCur, args.image, img_details)