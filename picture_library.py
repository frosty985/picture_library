import argparse
from argparse import RawTextHelpFormatter
import os.path
import configparser
import pymysql

import cat
import mysql_actions
import face_rec

from exif import imgDetails

"""
Main program for face detection and recognition

Options in config.ini

[database]
; self explanatory
user: username
pass: password
host: localhost
data: database

[faces]
; minimum percentage of confidence that a face has been recognised
min_conf: 65

[debug]
; print debug messages to the command line
messages: off
; display images, face detection, face recognition and conf%
display: off

"""


""" Set program arguments """
parser = argparse.ArgumentParser("Process image files and catalog them into a database", formatter_class=RawTextHelpFormatter)
parser.add_argument("image", type=str)
parser.add_argument("-a", "--action", type=str, default="all", help="Action to do:\n" +
                                                                    "(a)ll (default),\n" +
                                                                    "(d)atabase: insert to database,\n" +
                                                                    "fa(c)e: facial regonisation,\n" +
                                                                    "de(t)ect: detect faces for training data, use with -o --out\n"+
                                                                    "(r)efresh: images in the database")
parser.add_argument("-o", "--outdir", type=str, default="/tmp/piclib", help="Output directory")
parser.add_argument("-c", "--config", type=str, default="config.ini", help="Location of config file")

args = parser.parse_args()
configFileName = args.config


""" Set Golbal varibles """
config = None
con_database = None
con_debug = None
min_conf = None
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

    if con_debug.getboolean("messages"):
        debug = True
    else:
        debug = False

    con_min_conf = config["face"]
    min_conf = float(con_min_conf["min_conf"])

except:
    print("\nError reading config file.\nPlease check it is valid, and try again\n")
    exit()

""" Connect to MySQL database """
try:
    mysqlConnection = pymysql.connect(host=con_database["host"],
                                      user=con_database["user"],
                                      db=con_database["data"],
                                      passwd=con_database["pass"],
                                      autocommit=True,
                                      cursorclass=pymysql.cursors.DictCursor)
    mysqlCur = mysqlConnection.cursor()
except:
    print("\nThere was an error connecting to the MySQL database.\nPlease check your config file and try again.\n")
    exit()


def add_cat(filename, img_cat):
    #if img_cat is None:
    #    img_cat = "Uncatagorised"
    if debug:
        print("[Debug]\t" + filename + " is found to be: " + str(img_cat))

    """ Insert into database """
#    insert_file(str(filename), img_cat)

    if debug:
        print("[Debug]\tSetting cat in database")

    """ remove "not categorised" from link table if is there """
    mysql_actions.remove_notcat(mysqlCur, filename, debug=debug)
    """ insert in cat """
    mysql_actions.set_con(mysqlCur, filename, img_cat, debug=debug)


def insert_file(filename, img_cat=None, debug=False):
    """
    Insert filename into database
    :param filename:
    :param cat:
    :param debug:
    :return:
    """
    if img_cat is None:
        img_cat = "Uncatagorised"
    img_details = imgDetails(filename)
    if debug:
        print("[Debug]\t" + str(img_details))
        print("[Debug]\t Atempting to insert into database")
    mysql_actions.insert_file(mysqlCur, filename, img_details, debug=debug)
 #   mysql_actions.set_con(mysqlCur, filename, cat, debug=debug)
    add_cat(filename, img_cat)


""""
Detect faces for training
open image and detect faces (called from cat)
[ currently only looking for faces. future versions will be able to detect other objects ]
insert the filename and cat details into the database
"""
# TODO Add more object dection types


if args.action == "a" or args.action == "all":
    img_cat = None
    if debug:
        print("[Debug]\tRunning all actions")

    img_cat = cat.is_face(args.image, outdir=args.outdir, debug=debug, show=show)
    if debug:
        print("[Debug]\tPicture has cat of : " + str(img_cat))

    insert_file(str(args.image), str(img_cat))
    add_cat(args.image, img_cat)
    if img_cat is not None:
        face_rec.face_rec(args.image, mysqlCur, debug=debug, show=show)


elif args.action == "t" or args.action == "detect":
    if debug:
        print("[Debug]\tRunning only detecting faces")

    img_cat = cat.is_face(args.image, outdir=args.outdir, debug=debug, show=show)
    if debug:
        print("[Debug]\tPicture has cat of : " + str(img_cat))
    add_cat(args.image, str(img_cat))

elif args.action == "c" or args.action == "regcon":
    """ Run facial recognition on image """
    if debug:
        print("[Debug]\tStarting facial recognition")
    face_rec.face_rec(args.image, mysqlCur, debug=debug, show=show)

elif (args.action == "D" or args.action == "database"):
    """ Insert into database with no cat (just add the file) """
    img_cat = str(cat.is_face(args.image, outdir=args.outdir, debug=debug, show=show))
    insert_file(str(args.image), img_cat)

# todo Add option to process database, loop through filenames, add cat, dectect faces
# img_cat = cat.is_face(args.image, outdir=args.outdir, debug=debug, show=show)
# add_cat(args.image, str(img_cat))
