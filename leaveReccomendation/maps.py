import requests
import json

src = "-6.360052,106.832965"
# dest = "-6.364214,106.828713"
dest = "-6.224380,106.809943"
sub_key = "xeRkgAk2OG8sjZgPxuwfkF1-h03FKIH5ErhCjxHaL7c"
url = "https://atlas.microsoft.com/route/directions/json?subscription-key={}&api-version=1.0&query={}:{}&travelMode=car".format(sub_key, src, dest)
r = requests.get(url)
r = json.loads(r.text)
# print(json.dumps(r, indent=4, sort_keys=True))
r = r["routes"]
for x in r:
    x = x["summary"]
    time = x["travelTimeInSeconds"]
    dist = x["lengthInMeters"]
    print('dist:', dist/1000, 'km')
    print('time:', time/60, 'minute')