# This is a simple script for temporarily disabling pi-hole DNS filtering.
# Last updated for pi-hole 6.4

import os
import requests

PI_HOLE_IP_ADDRESS = os.getenv('PI_HOLE_IP_ADDRESS')
PI_HOLE_APP_PASSWORD = os.getenv('PI_HOLE_APP_PASSWORD')
PI_HOLE_DISABLE_TIME_IN_SEC = int(os.getenv('PI_HOLE_DISABLE_TIME_IN_SEC', 60))
PI_HOLE_API_URL = f"http://{PI_HOLE_IP_ADDRESS}/api"

def main():
    response = requests.post(
        url = f"{PI_HOLE_API_URL}/auth",
        json = {
            'password': PI_HOLE_APP_PASSWORD
        }
    )

    response.raise_for_status()
    data = response.json()
    sid = data['session']['sid']

    response = requests.post(
        url = f"{PI_HOLE_API_URL}/dns/blocking",
        json = {
            'sid': sid,
            'blocking': False,
            'timer': PI_HOLE_DISABLE_TIME_IN_SEC
        }
    )

    response.raise_for_status()
    
    response = requests.delete(
        url = f"{PI_HOLE_API_URL}/auth",
        json = {
            'sid': sid
        }
    )

    response.raise_for_status()
    print("Success!")

if __name__ == '__main__':
    main()
