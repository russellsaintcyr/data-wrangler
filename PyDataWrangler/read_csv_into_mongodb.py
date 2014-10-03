# script to open a URL, download an archive file, unzip, read in each file, 
# and insert into a MongoDB NoSQL database
import csv # for file parsing
import pymongo # for access to Mongo in Python
import time # for timestamp
import os # for regex parsing of file name
import locale # for readibility of large numbers
import sys # for the arguments
import logging # for debugging
import urllib # for remote file download
import zipfile # to handle archives

# first ensure we have some arguments
if len(sys.argv) == 4:
    # TODO: error-checking for file_name argument
    mongo_url = sys.argv[1]
    database_name = sys.argv[2]
    file_name_or_url = sys.argv[3]
else:
    usage = "Usage: mongo_url database_name file_name_or_url"
    sys.stderr.write(usage)
    exit()

# timestamp to report on total script execution time
startTime = time.time()
# local variables and config
delimiter = ','
quote_character = '"'
locale.setlocale(locale.LC_ALL, 'en_US.utf8')
LOG_FILENAME = 'logs/read_CSV.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)
logToFile = True
def log(msg):
    if logToFile == True:
        logging.debug(msg)
    print msg
def logerror(msg):
    if logToFile == True:
        logging.error(msg)
    sys.stderr.write(msg)

# try connecting to db
try:
    log("Connecting to database %s at %s..." % (database_name, mongo_url))
    connection = pymongo.MongoClient(mongo_url)
    log("... Connected.")
    db = connection[database_name] # will create database if it isn't there
except:
    logerror("... Failed to connect.")
    exit()

# functions
def read_in_file(file_name):
    # extract collection name from the file
    coll_name = os.path.splitext(os.path.basename(file_name))[0]
    # try opening file
    try:
        log("Opening file at %s..." % file_name)
        csv_fp = open(file_name, 'rb') # rb = reading binary
        log("... Opened file.")
    except:
        logerror("... Failed to open file.")
        exit()
    reader = csv.DictReader(csv_fp, delimiter=delimiter, quotechar=quote_character)
    current_row = 0
    for row in reader:
        current_row += 1
        collection = db[coll_name] # will create collection if doesn't exist
        collection.insert(row)
        # nicely format the row
        rownum = locale.format("%d", current_row, grouping=True)
        # give feedback after every X inserts. useful for very large files.
        if current_row % 1000 == 0:
            log("... inserted row %s in '%s' collection ..." % (rownum,coll_name))
        #log("Inserted to %s: %s " % (coll_name,row)
    log("Finished reading local file at %s." % file_name)
    # compute and report end time
    elapsedTime = time.time() - startTime
    log("Processed %s lines in %s seconds." % (rownum, '{0:.3g}'.format(elapsedTime)))

# is this a URL or a local CSV
if file_name_or_url[0:4] == 'http':
    remote_file = urllib.URLopener()
    try:
        # mkdir for downloaded data
        if not os.path.exists('downloads'):
            log("Making directory for downloads")
            os.makedirs('downloads')
        # TODO: extract filename from end of URL
        log("Retrieving file from %s..." % file_name_or_url)
        remote_file.retrieve(file_name_or_url, "downloads/remote_archive.zip")
        log("... Retrieved file.")
    except:
        logerror("... Failed to retrieve file.")
    # extract files
    zipf = zipfile.ZipFile("downloads/remote_archive.zip", mode='r')
    extracted_data_dir = 'extracted_data'
    if not os.path.exists(extracted_data_dir):
        log("Making directory %s." % extracted_data_dir)
        os.makedirs(extracted_data_dir)
    for subfile in zipf.namelist():
        zipf.extract(subfile, extracted_data_dir)
    log("Extracted files to %s." % extracted_data_dir)
    # loop through the extracted files
    for root, dirs, files in os.walk(extracted_data_dir, topdown=False):
        log("Looping through files.")
        for name in files:
            read_in_file(os.path.join(root, name))
else:
    read_in_file(file_name_or_url)
# done
