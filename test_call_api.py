import os

import requests
from requests.auth import HTTPBasicAuth

if __name__ == "__main__":
    #USER = os.environ["UN"]
    #PASS = os.environ["PW"]
    
    #basic = HTTPBasicAuth(USER, PASS)

    #r = requests.get("https://hirenick.pythonanywhere.com/get_last_n_signals/25", auth=basic)

    # Replace URL with that of your web app
    r = requests.get("https://hirenick.pythonanywhere.com/get_last_n_signals/25")

    if r.status_code == 200:
        print("Good Status Code Returned")
        as_json = r.json()

        print(as_json)

    else:
        print(r.status_code)
        print(r.text)