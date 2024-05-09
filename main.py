import os
import requests
import creds
import time
from twilio.rest import Client

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

Author: Alex Powell     Version: 1.0.3
"""

test_mode = False


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
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        return update_order_status()
    else:
        try:
            date_created = order_details['date_created']
            status = order_details['status']
            item_count = order_details['items_total']
            total = float(order_details['total_inc_tax'])
            total = f"${"%.2f" % total}"
            first_name = order_details['billing_address']['first_name']
            last_name = order_details['billing_address']['last_name']
            phone = order_details['billing_address']['phone']
        except KeyError:
            print("Order Not Found!")
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            return update_order_status()
        else:
            return date_created, status, item_count, total, first_name, last_name, phone


def format_phone(phone_number, mode="Twilio", prefix=True):
    """Cleanses input data and returns masked phone for either Twilio or Counterpoint configuration"""
    phone_number_as_string = str(phone_number)
    # Strip away extra symbols
    formatted_phone = phone_number_as_string.replace(" ", "")  # Remove Spaces
    formatted_phone = formatted_phone.replace("-", "")  # Remove Hyphens
    formatted_phone = formatted_phone.replace("(", "")  # Remove Open Parenthesis
    formatted_phone = formatted_phone.replace(")", "")  # Remove Close Parenthesis
    formatted_phone = formatted_phone.replace("+1", "")  # Remove +1
    formatted_phone = formatted_phone[-10:]  # Get last 10 characters
    if mode == "Counterpoint":
        # Masking ###-###-####
        cp_phone = formatted_phone[0:3] + "-" + formatted_phone[3:6] + "-" + formatted_phone[6:10]
        return cp_phone
    else:
        if prefix:
            formatted_phone = "+1" + formatted_phone
        return formatted_phone


def send_text(order_number, name, phone_number):
    message = (f"{creds.business_name}: Hello {name}! Order {order_number} is ready for pickup at {creds.address}. "
               f"Our hours are {creds.hours}. See you soon!")
    client = Client(creds.account_sid, creds.auth_token)
    client.messages.create(from_=creds.TWILIO_PHONE_NUMBER, to=phone_number, body=message)


def update_order_status():
    print(art)
    order_id = input("Enter order ID: ")
    if order_id != "":
        if test_mode:
            date_created, status, item_count, total, first_name, last_name, phone = \
                creds.dummy_data
        else:
            date_created, status, item_count, total, first_name, last_name, phone = get_order_details(order_id)
            print(f"\nDate Created: {date_created[:-6]}")
            print(f"Name: {first_name} {last_name}")
            print(f"Phone: {format_phone(phone, mode="Counterpoint")}")
            print(f"Status: {status}")
            print(f"Item Count: {item_count}")
            print(f"Total: {total}\n")

        mode = input("Press 1 for 'Awaiting Pickup'\nPress 2 for 'Complete'\nPress 3 to reset\nResponse:")

        # Barcode Scanner Double Enter Fix # 2
        if mode == "":
            mode = input("")

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
                print(f"\nOrder {order_id} has been updated to Awaiting Pickup")
                send_text(order_id, first_name, format_phone(phone, prefix=True))
                print(f"\nText notification has been sent to {format_phone(phone, mode="Counterpoint")}\n")
                time.sleep(1)
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
                    time.sleep(1)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    update_order_status()
                elif archive == "n":
                    print(f"\nOrder {order_id} has been updated to 'Complete'.\n")
                    time.sleep(1)
                    os.system('cls' if os.name == 'nt' else 'clear')

                    update_order_status()
                else:
                    print("Invalid response. Please try again.\n")
                    time.sleep(1)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    update_order_status()

        elif mode == "3":
            print("Resetting.\n")
            time.sleep(.5)
            os.system('cls' if os.name == 'nt' else 'clear')
            update_order_status()

        else:
            print("Invalid response. Please try again.\n")
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            update_order_status()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        update_order_status()


update_order_status()
