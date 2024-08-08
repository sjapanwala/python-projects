## /\/\ Start Of Imports /\/\

import getpass
import requests
import json
import sys
import os
from os import system
import subprocess
import platform
USERNAME = getpass.getuser()
DEVICE = platform.node()

## /\/\ End Of Imports /\/\

def get_userip():
    response = requests.get("https://www.icanhazip.com")

    # Check if the request was successful
    if response.status_code == 200:
        user_ip = response.text.strip()  # Strip any trailing newline characters
    else:
        print(f"Failed to fetch IP address. Status code: {response.status_code}")
        print(f"Error message: {response.text}")
    return user_ip

def get_ipinfo(target_ip):
    response = requests.get(f"http://ip-api.com/json/{target_ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,asname,reverse,mobile,proxy,hosting,query")
    return response.json()

def base_list(ip_info):
    if ip_info["status"] == "success":
        # Accessing all properties
        status = ip_info["status"]
        country = ip_info["country"]
        countryCode = ip_info["countryCode"]
        region = ip_info["region"]
        regionName = ip_info["regionName"]
        city = ip_info["city"]
        zip_code = ip_info["zip"]
        lat = ip_info["lat"]
        lon = ip_info["lon"]
        timezone = ip_info["timezone"]
        isp = ip_info["isp"]
        org = ip_info["org"]
        as_ = ip_info["as"]
        asname = ip_info["asname"]
        reverse = ip_info["reverse"]
        mobile = ip_info["mobile"]
        proxy = ip_info["proxy"]
        hosting = ip_info["hosting"]
        query = ip_info["query"]

        # Prepare the table
        data = [
            ("Status", status),
            ("Country", country),
            ("Country Code", countryCode),
            ("Region", region),
            ("Region Name", regionName),
            ("City", city),
            ("ZIP Code", zip_code),
            ("Latitude", lat),
            ("Longitude", lon),
            ("Timezone", timezone),
            ("ISP", isp),
            ("Organization", org),
            ("AS", as_),
            ("AS Name", asname),
            ("Reverse", reverse),
            ("Mobile", mobile),
            ("Proxy", proxy),
            ("Hosting", hosting),
            ("Query", query),
            ("Username", USERNAME),
            ("Device Name", DEVICE)
        ]

        # Calculate the maximum length of the first column
        max_key_length = max(len(key) for key, _ in data)
        max_value_length = max(len(str(value)) for _, value in data)
        
        print("|" + (max_value_length + max_key_length + 5) * "-" + "|")
        # Print the table header
        print(f"| {'Key':<{max_key_length}} | {'Value':<{max_value_length}} |")
        print(f"| {'-' * max_key_length} | {'-' * max_value_length} |")

        # Print the table rows
        for key, value in data:
            print(f"| {key:<{max_key_length}} | {value:<{max_value_length}} |")
        print("|" + (max_value_length + max_key_length + 5) * "-" + "|")
    else:
        print(f"Error: {ip_info['message']}")
        pass

        
def cool_fetch(ip_info):
    user_string = USERNAME+"@"+DEVICE
    userline = len(user_string) * "-"
    print(f"\n     b.          {user_string}")
    print(f"\033[0m     88b         {userline}")
    print(f"\033[0m     888b        \033[91m󰍍  {ip_info['country']} ")
    print(f"\033[0m     88888b      \033[92m  {ip_info['city']}")
    print(f"\033[0m     888888b.    \033[93m  {ip_info['regionName']}")
    print(f"\033[0m     8888P'      \033[94m  {ip_info['zip']}...")
    print(f"\033[0m     P' `8.      \033[95m󰢍  {ip_info['isp']}")
    print(f"\033[0m         `8.     \033[96m  {ip_info['query']}")
    print(f"\033[0m          `8     \033[97m  {ip_info['timezone']}\033[0m\n")
    #return ip_info['status']

def help():
    print("Recognised Args\n '-?'     Help\n '-bf'    Base Fetch \n '-cf'    Curser Fetch\n")
    print("\n for custom ip's add ip after an arg")

def main():
    user_ip =  get_userip()
    ipinfo = get_ipinfo(user_ip)
    if len(sys.argv) > 1 and sys.argv[1] == "-bl":
        if len(sys.argv) > 2 and sys.argv[2] != "":
            ipinfo = get_ipinfo(sys.argv[2])
            base_list(ipinfo)
        else:
            base_list(ipinfo)
    elif len(sys.argv) > 1 and sys.argv[1] == "-cf":
            if len(sys.argv) > 2 and sys.argv[2] != "":
                ipinfo = get_ipinfo(sys.argv[2])
                cool_fetch(ipinfo)
            else:
                cool_fetch(ipinfo)
    elif len(sys.argv) > 1 and sys.argv[1] == "-?":
        help()
    else:
        print("Unrecognized Arg\nTry '-?'")

if __name__ == "__main__":
    main()
