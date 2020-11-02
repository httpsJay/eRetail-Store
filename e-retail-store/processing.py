import uuid
from collections import OrderedDict
import json
import os
import threading
import urllib
from PIL import Image
from random import randint
from time import sleep
from datetime import datetime, timedelta
from multiprocessing import Queue
from database_defines import *

#global queue
queue_obj  = Queue()


# visit_view = OrderedDict()
# visit_view["store_id"]      = ""
# visit_view["area"]          = ""
# visit_view["store_name"]    = ""
# visit_view["data"]          = []



#Visit_Info_Return
def construct_return (value, job_to_visit_dict):
    #JAY - new
    if value["store_id"] not in job_to_visit_dict.keys():
        data = {}
        data_list = []

        visit_view = OrderedDict()
        visit_view["store_id"] = ""
        visit_view["area"] = ""
        visit_view["store_name"] = ""
        visit_view["data"] = []

        job_to_visit_dict[str(value["store_id"])] = visit_view
        job_to_visit_dict[str(value["store_id"])]["store_id"] = value["store_id"]

        data_part = data
        data_part["date"]          = value["visit_time"]
        data_part["perimeter"]     = value["perimeter"]
        data_part["job_id"]        = value["job_id"]
        data_list.append(data_part)
        job_to_visit_dict[str(value["store_id"])]["data"] = data_list


    #if there is jobs in list
    else:
        if len(job_to_visit_dict[str(value["store_id"])]["data"]):
            for item in job_to_visit_dict[str(value["store_id"])]["data"]:
                if item["job_id"] == value["job_id"]:
                    old_perimeter = int(item["perimeter"])
                    new_perimeter = old_perimeter + int(value["perimeter"])
                    item["perimeter"] = str(new_perimeter)
                    break
        else:
            data_part = {}
            data_part["date"]          = value["visit_time"]
            data_part["perimeter"]     = value["perimeter"]
            data_part["job_id"]        = value["job_id"]
            job_to_visit_dict[str(value["store_id"])]["data"].append(data_part)

    # IMAGES database
    stores_txn = stores_db_env.begin(write=True, buffers=True,  db=stores_subdb)
    stores_cursor = stores_txn.cursor()
    store_value = stores_cursor.get(str(value["store_id"]).encode())
    store_value = eval(str(store_value))
    stores_txn.commit()
    #now store db related variables are being captured 
    job_to_visit_dict[str(value["store_id"])]["area"] = store_value["area_code"]
    job_to_visit_dict[str(value["store_id"])]["store_name"] = store_value["store_name"]

    return job_to_visit_dict

#----------------------------------------------------------------------------
def assign_job_id():
    return uuid.uuid1()

def job_id_cache(job_id):
    try:
        txn = jobs_db_env.begin(write=True, buffers=True, db=jobs_subdb)
        # cursor = txn.cursor()
        value = {}
        value["status"] = "ongoing"
        value["store_id_list"] = ""
        value["store_id_failed"] = ""
        # value["created_at"] = str(datetime.now())
        # value["modified_at"] = str(datetime.now())

        txn.put(str(job_id).encode(), str(value))
        txn.commit()
    except Exception as e:
        print("Exception : ", e)
        return 1
    return 0

def processing_task (job_id, visits):
        #JAY - Test
        print("processing_task () : ", threading.currentThread().getName())
        print("queue get : ", datetime.now())
        test_start_time = datetime.now()
        # insert the new store jobs record in database
        store_list = []
        failed_store_list = []

        for store in  visits:
            store_list.append(str(store['store_id']))

            dir_file = 'image_downloads/' + \
                str( job_id) + '/' + \
                store['store_id'] + '/' + \
                store['visit_time']

            if not os.path.exists(dir_file):
                os.makedirs(dir_file)

            for image_url in store['image_url']:
                try:
                    urllib.urlretrieve(image_url, dir_file + '/'+image_url.split("/")[-1])

                    current_image = Image.open(
                        dir_file + '/'+image_url.split("/")[-1])
                    width, height = current_image.size
                    perimeter = 2*(width + height)

                    #Add details to IMAGE db
                    image = {}
                    image["job_id"]         = str(job_id)
                    image["store_id"]       = str(store['store_id'])
                    # image["img_url"]        = str(image_url)
                    image["perimeter"]      = str(perimeter)
                    image["visit_time"]     = str(store['visit_time'])
                    image = json.dumps(image)

                    #update lmdb cache - onging to completed
                    txn = images_db_env.begin(write=True, buffers=True, db=images_subdb)
                    txn.put(str(image_url).encode(), str(image))
                    txn.commit()
                    sleep(randint(1, 4)/10)
                    #JAY - Test
                    print("Image : ",threading.currentThread().getName())

                except Exception as e:
                    failed_store_list.append(str(store['store_id']))
                    print(
                        "Image Link Broken: Not stopping the processing as every Data is Important")


            if failed_store_list:
                status = "failed"
            else:
                status = "completed"

            #create value
            value = {}
            value["status"]             = status
            value["store_id_list"]      = store_list
            value["store_id_failed"]    = failed_store_list
            value["created_at"]         = datetime.now().strftime("%m-%d-%YT%H:%M:%S")
            value["modified_at"]        = datetime.now().strftime("%m-%d-%YT%H:%M:%S")

            value = json.dumps(value)

            #update lmdb cache - onging to completed
            txn = jobs_db_env.begin(write=True, buffers=True, db=jobs_subdb)
            txn.put(str(job_id).encode(), str(value))
            txn.commit()

        #JAY - Test
        print("task-completed - ",threading.currentThread().getName()," -- Job ID : ", str(job_id))
        # print("---Completion Time date time : ",datetime.now() - test_start_time)
        print(datetime.now())

def read_to_process ():
    while 1:
        try:
            evlog_info = queue_obj.get(block = True)

            job_id = evlog_info[0]
            visits = evlog_info[1]
            processing_task (job_id, visits)
        except Exception as e:
            print("Exception : ", e)


#putting in queue
def queue_put(jobid, visits):
    #JAY - Test
    print("queue put : ", datetime.now())
    queue_obj.put([jobid, visits])


def thread_init ():
        try:
            #creating and calling multiple threads for fetching jobs
            #we are using Python threading.
            #For better speedup in production Process can be used. Should work fine.
            #Need Proper Performance Testing
            evlogthread1 = threading.Thread(name='thread1', target= read_to_process)
            evlogthread1.start()

            evlogthread2 = threading.Thread(name='thread2', target= read_to_process)
            evlogthread2.start()

            evlogthread3 = threading.Thread(name='thread3', target= read_to_process)
            evlogthread3.start()


        except Exception as e:
            print("Exception in initialising event logging thread {}".format(e))


#Starting the Queue through thread
thread_init()
