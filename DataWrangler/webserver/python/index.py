import bottle
from pymongo import MongoClient

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
    return bottle.template('collections', dict(collections = collections), dbname=dbname)

@bottle.route('/db/<dbname>/<collname>')
def show_collection(dbname,collname):
    db = client[dbname]
    collection = db[collname]
    cursor = collection.find()
    print cursor.count
    for each_name in cursor:
        print each_name
    return bottle.template('collection', dbname=dbname, collname=collname)

bottle.debug(True)
bottle.run(host='localhost', port=8080)
