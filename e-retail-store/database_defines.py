import lmdb
import csv

#DATABASES : JOBS, IMAGES, STORES
#LMDB database for job-status - JOBS
try:
    jobs_db_path = './database/jobs_db'
    jobs_db_env = lmdb.open(jobs_db_path, max_dbs=1)
    jobs_subdb = jobs_db_env.open_db("jobs")
except Exception as e:
    print("exception in JOBS database : ", e)

#LMDB database for job-status - IMAGES
try:
    images_db_path = './database/images_db'
    images_db_env = lmdb.open(images_db_path, max_dbs=1)
    images_subdb = images_db_env.open_db("images")
except Exception as e:
    print("exception in IMAGES database : ", e)

#LMDB database for job-status - STORES
try:
    stores_db_path = './database/stores_db'
    stores_db_env = lmdb.open(stores_db_path, max_dbs=1)
    stores_subdb = stores_db_env.open_db("stores")

    #setup database from csv
    txn = stores_db_env.begin(write=True, buffers=True, db=stores_subdb)
    filename = "StoreMasterAssignment.csv"

    # opening the file using "with"
    # statement
    with open(filename, 'r') as data:
        for line in csv.DictReader(data):
            # print(line["StoreID"])
            # store_name
            # area_code
            value = {}
            value["area_code"] = line["AreaCode"]
            value["store_name"] = line["StoreName"]
            txn.put(str(line["StoreID"]).encode(), str(value))

    txn.commit()
except Exception as e:
    print("exception in STORES database : ", e)
