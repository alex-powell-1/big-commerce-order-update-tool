import os
import requests
import creds
import time

"""
BigCommerce Order Update Tool
Author: Alex Powell
Written: January 19, 2024

"""
client_id = creds.client_id
access_token = creds.access_token
store_hash = creds.store_hash
art = r"""
   ___          _             _   _           _       _       
  / _ \ _ __ __| | ___ _ __  | | | |_ __   __| | __ _| |_ ___ 
 | | | | '__/ _` |/ _ \ '__| | | | | '_ \ / _` |/ _` | __/ _ \
 | |_| | | | (_| |  __/ |    | |_| | |_) | (_| | (_| | ||  __/
  \___/|_|  \__,_|\___|_|     \___/| .__/ \__,_|\__,_|\__\___|
                                   |_|                        

Author: Alex Powell     Version 1.0
"""


def get_order_details(order_id):
    url = f" https://api.bigcommerce.com/stores/{store_hash}/v2/orders/{order_id}"
    headers = {
        'X-Auth-Token': access_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    order_details = (requests.get(url, headers=headers)).json()

    if order_details == [{'status': 404, 'message': 'The requested resource was not found.'}]:
        print("Order Not Found!")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        return update_order_status()
    else:
        date_created = order_details['date_created']
        status = order_details['status']
        item_count = order_details['items_total']
        total = float(order_details['total_inc_tax'])
        total = f"${"%.2f" % total}"
        first_name = order_details['billing_address']['first_name']
        last_name = order_details['billing_address']['last_name']
        return date_created, status, item_count, total, first_name, last_name


def update_order_status():
    print(art)
    order_id = input("Enter order ID: ")
    date_created, status, item_count, total, first_name, last_name = get_order_details(order_id)
    print(f"\nDate Created: {date_created}")
    print(f"Name: {first_name} {last_name}")
    print(f"Status: {status}")
    print(f"Item Count: {item_count}")
    print(f"Total: {total}\n")

    mode = input("Press 1 for 'Awaiting Pickup'\nPress 2 for 'Complete'\nResponse: ")

    if mode == "1" or mode == "2":
        url = f" https://api.bigcommerce.com/stores/{store_hash}/v2/orders/{order_id}"
        headers = {
            'X-Auth-Token': access_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if mode == "1":
            payload = {
                "status_id": 8,
            }
            requests.put(url, headers=headers, json=payload)
            print(f"\nOrder {order_id} has been updated to Awaiting Pickup\n")
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')
            update_order_status()

        if mode == "2":
            payload = {
                "status_id": 10,
            }
            requests.put(url, headers=headers, json=payload)
            archive = input("Archive order? Y or N: ").lower()
            if archive == "y":
                requests.delete(url, headers=headers)
                print(f"\nOrder {order_id} has been updated to 'Complete' and archived.\n")
                time.sleep(2)
                os.system('cls' if os.name == 'nt' else 'clear')
                update_order_status()
            elif archive == "n":
                print(f"\nOrder {order_id} has been updated to 'Complete'.\n")
                time.sleep(2)
                os.system('cls' if os.name == 'nt' else 'clear')
                update_order_status()
            else:
                print("Invalid response. Please try again.\n")
                time.sleep(2)
                os.system('cls' if os.name == 'nt' else 'clear')
                update_order_status()
    else:
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        update_order_status()


update_order_status()
