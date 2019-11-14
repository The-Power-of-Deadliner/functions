import logging

import azure.functions as func

import json

import psycopg2

import requests

def get_dist_time(src, dest, vehicle='car'):
    sub_key = "xeRkgAk2OG8sjZgPxuwfkF1-h03FKIH5ErhCjxHaL7c"
    url = "https://atlas.microsoft.com/route/directions/json?subscription-key={}&api-version=1.0&query={}:{}&travelMode={}".format(sub_key, src, dest, vehicle)
    r = requests.get(url)
    r = json.loads(r.text)
    # print(json.dumps(r, indent=4, sort_keys=True))
    r = r["routes"]
    for x in r:
        x = x["summary"]
        time = x["travelTimeInSeconds"]
        dist = x["lengthInMeters"]
    return dist, time

def get_leaves():
    host = "hike-a-thon-postgres.postgres.database.azure.com"
    dbname = "postgres"
    user = "aabccd021@hike-a-thon-postgres"
    password = "hike-a-thon11"
    sslmode = "require"

    # Construct connection string
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    conn = psycopg2.connect(conn_string) 
    print("Connection established")

    cursor = conn.cursor()

    # Fetch all rows from table
    cursor.execute("SELECT * FROM leave;")
    rows = cursor.fetchall()

    times = []
    for row in rows:
        veh = 'car' if row[6]=='mobil' else 'motorcycle'
        dist, time = get_dist_time(row[3], row[4], veh)
        time = {
            'source' : str(row[0]),
            'dest' : str(row[1]),
            'cost' : row[2],
            'source_c' : row[3],
            'dest_c' : row[4],
            'schedule' : row[5],
            'vehicle' : veh,
            'distance' : dist,
            'duration' : time,
        }
        times.append(time)


    # Cleanup
    conn.commit()
    cursor.close()
    conn.close()
    return times



def main(req: func.HttpRequest) -> func.HttpResponse:

    recommendation = {
        'leavingTimes' : get_leaves()   }

    ret = json.dumps(recommendation)

    ret = str(ret)

    return func.HttpResponse(ret)
    # logging.info('Python HTTP trigger function processed a request.')

    # name = req.params.get('name')
    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')

    # if name:
    #     return func.HttpResponse(f"Hello {name}!")
    # else:
    #     return func.HttpResponse(
    #          "Please pass a name on the query string or in the request body",
    #          status_code=400
    #     )
