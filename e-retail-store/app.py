"""
    Flask Server
"""
# import necessary libraries
from flask import Flask, jsonify, request
from processing import *

# creating a Flask app
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    default = "Hey!!! Service is Up-n-Running"
    return jsonify({'data': data})

#route for submit api
@app.route('/api/submit', methods=['POST'], strict_slashes=False)
def submit_job():
    request_data = request.json
    try:
        if request_data['count'] and request_data['visits']:
            if(request_data['count'] != len(request_data['visits'])):
                response = jsonify({
                    "error": "Invalid fields in the request"
                })
                response.status_code = 400
                return response
            else:
                #assign job_id
                job_id = assign_job_id()
                #collect job_id for status info
                err = job_id_cache(job_id)
                if err:
                    print("Error : Caching job-id")

                #JAY - Test
                print("Putting In queue - Job ID : ", str(job_id), "--", datetime.now())

                #process job
                queue_put(job_id, request_data['visits'])

                # return the response
                response = jsonify({
                    "job_id": job_id
                })
                response.status_code = 201
                return response #ff44864c-17df-11eb-8dda-000c29c626fa
    except KeyError:
        # missing values and incorrect request
        response = jsonify({
            "error": "Invalid request"
        })
        response.status_code = 400
        return response
    except:
        response = jsonify({"error": "Something went wrong"})
        response.status_code = 400
        return response

#route for status api
@app.route('/api/status', methods=['GET'], strict_slashes=False)
def job_status():
    job_id = request.args.get('jobid')
    if(str(job_id)):
        try:
            txn = jobs_db_env.begin(write=True, buffers=True,  db=jobs_subdb)
            cursor = txn.cursor()
            value = cursor.get(str(job_id).encode())
            txn.commit()

            if value != None:
                value = eval(str(value))
                if (value['status'] is 'completed') or (value['status'] is 'ongoing'):
                    response = jsonify({
                        "status": value['status'],
                        "job_id": str(job_id)
                    })
                    response.status_code = 200
                    return response
                #for failed status
                else:
                    response = jsonify({
                        "status": value['status'],
                        "job_id": str(job_id),
                        "error": [{
                            "store_id": str(value["store_id"])
                        }]
                    })
                    response.status_code = 200
                    return response
            #when no job_id found
            else:
                response = jsonify({
                })
                response.status_code = 400
                return response

        except Exception as e:
            response = jsonify({"error": "Unexpected Exception : "})
            response.status_code = 400
            return response
    else:
        # if jobid is not mentioned in the request
        response = jsonify({
            "error": "job_id not mentioned"
        })
        response.status_code = 400
        return response

#route for visit api
@app.route('/api/visits', methods=['GET'], strict_slashes=False)
def visit_info():
    area_code = request.args.get('area')
    store_id = request.args.get('storeid')
    start_date = request.args.get('startdate')
    end_date = request.args.get('enddate')

    filter_store_list = []
    job_to_visit_dict = {}

    #Will not search areacode if store_id filter is used
    if store_id is None:
        if area_code != None:
            # STORES database
            txn = stores_db_env.begin(write=True, buffers=True,  db=stores_subdb)
            cursor = txn.cursor()

            for key1, value1 in cursor:
                if eval(str(value1))["area_code"] == area_code:
                    filter_store_list.append(str(key1))

            txn.commit()
    #store_id is used in filter
    else:
        filter_store_list = []
        filter_store_list.append(str(store_id))

    # IMAGES database
    images_txn = images_db_env.begin(write=True, buffers=True,  db=images_subdb)
    images_cursor = images_txn.cursor()

    for key, value in images_cursor:
        visit = eval(str(value))["visit_time"]
        value = eval(str(value))
        # value_job_id = value["job_id"]
        # value_store_id = value["store_id"]

        #when startdate and enddate both filter
        if (start_date != None) and (end_date != None):

            if visit >= start_date and visit <= end_date:
                if filter_store_list:
                    if value["store_id"] in filter_store_list:
                        job_to_visit_dict = construct_return (value, job_to_visit_dict)
                    else:
                        print("Not Matched")
                else:
                    job_to_visit_dict = construct_return (value, job_to_visit_dict)
            else:
                print("Not Matched")

        #when only startdate filter
        elif start_date != None:
            if visit >= start_date:
                if filter_store_list:
                    if value["store_id"] in filter_store_list:
                        job_to_visit_dict = construct_return (value, job_to_visit_dict)
                    else:
                        print("Not Matched")
                else:
                    job_to_visit_dict = construct_return (value, job_to_visit_dict)
            else:
                print("Not Matched")

        #when only enddate filter
        elif end_date != None:
            if visit <= end_date:
                if filter_store_list:
                    if value["store_id"] in filter_store_list:
                        job_to_visit_dict = construct_return (value, job_to_visit_dict)
                    else:
                        print("Not Matched")
                else:
                    job_to_visit_dict = construct_return (value, job_to_visit_dict)
            else:
                print("Not Matched")

        #when no date filter
        else :
            if filter_store_list:
                if value["store_id"] in filter_store_list:
                    job_to_visit_dict = construct_return (value, job_to_visit_dict)
                else:
                    print("Not Matched")
            else:
                construct_return (value, job_to_visit_dict)

    images_txn.commit()

    return_list = job_to_visit_dict.values()
    response = jsonify({
                "results": return_list})
    response.status_code = 200
    return response

# main function
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

