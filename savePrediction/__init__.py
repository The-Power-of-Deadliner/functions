import logging

import azure.functions as func
from azure.storage.blob import BlobClient
import pickle
import pandas as pd

blob = BlobClient(account_url="https://blobhikeathon.blob.core.windows.net",
                  container_name="blobcon",
                  blob_name="model.pkl",
                  credential="qC8kJ7CvBvoEDAFHrNy2E3VJNCKFXkEyh2wb2yozxOkN+r7yGBgYxMy+cwS8UjEjj7hm3+tQWAj0bzAp3YVZog==")

with open("model.pkl", "wb") as f:
    data = blob.download_blob()
    data.readinto(f)


model = pickle.load(open('model.pkl', 'rb'))

blob = BlobClient(account_url="https://blobhikeathon.blob.core.windows.net",
                  container_name="blobcon",
                  blob_name="test.csv",
                  credential="qC8kJ7CvBvoEDAFHrNy2E3VJNCKFXkEyh2wb2yozxOkN+r7yGBgYxMy+cwS8UjEjj7hm3+tQWAj0bzAp3YVZog==")

with open("test.csv", "wb") as f:
    data = blob.download_blob()
    data.readinto(f)

test = pd.read_csv('test.csv')
dummies = ['Vehicle Type']
features = ['Ride Distance (km)', 'Promo Value']+dummies
test = test[features].dropna().replace('-','0').rename(columns={'Ride Distance (km)': 'dist'})

for dummy in dummies:
    one_hot = pd.get_dummies(test[dummy])
    test = test.drop(dummy,axis = 1)
    test = test.join(one_hot)

test = test.drop('Promo Value', 1)

def main(req: func.HttpRequest) -> func.HttpResponse:

    return func.HttpResponse("{}".format(model.predict(test).sum()))
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
