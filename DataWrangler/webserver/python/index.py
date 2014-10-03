import bottle
from pymongo import MongoClient
import locale # for readibility of large numbers
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

client = MongoClient('localhost',27017)

@bottle.route('/')
def show_databases():
    # get array of db names
    dbs = client.database_names()
    return bottle.template('dbs', dict(databases = dbs))
    
@bottle.route('/db/<dbname>')
def show_collections(dbname):
    db = client[dbname]
    collections = db.collection_names()
    return bottle.template('collections', 
                           dict(collections = collections), 
                           dbname=dbname)

@bottle.route('/db/<dbname>/<collname>')
def show_collection(dbname,collname):
    db = client[dbname]
    collection = db[collname]
    cursor = collection.find()
    cursor.limit(10)
    return bottle.template('collection', 
                           dict(keys = collection.find_one()), 
                           dict(collection = cursor), 
                           dbname=dbname, 
                           collname=collname,
                           count=locale.format("%d", cursor.count(), grouping=True))

#bottle.debug(True)
bottle.run(host='localhost', port=8080)
