from azure.storage.blob import BlobClient
import pickle

blob = BlobClient(account_url="https://blobhikeathon.blob.core.windows.net",
                  container_name="blobcon",
                  blob_name="model.pkl",
                  credential="qC8kJ7CvBvoEDAFHrNy2E3VJNCKFXkEyh2wb2yozxOkN+r7yGBgYxMy+cwS8UjEjj7hm3+tQWAj0bzAp3YVZog==")

with open("model.pkl", "wb") as f:
    data = blob.download_blob()
    data.readinto(f)

model = pickle.load(open('model.pkl', 'rb'))
pred = model.predict([[6,1,0]])
print(pred)