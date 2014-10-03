Data Wrangler
=============
Downloads archived data from a remote source, extracts files locally, and inserts data into a new NoSQL database (at the moment using MongoDB but I will also test with Redis).

Tested with bus route data from OC Transpo, the transportation authority for the City of Ottawa.

The project structure can be imported into Eclipse as a PyDev project. 

To run, execute the file `read_csv_into_mongodb`. It takes 3 arguments:

1. The url for your MongoDB
2. The name of your database. It will be created if it doesn't exist.
3. The URL to the archive

Example usage:
```
python ./read_csv_into_mongodb.py mongodb://localhost ottawa http://www.octranspo1.com/files/google_transit.zip
```
This is very much a work in progress, but feedback and requests are welcome.
