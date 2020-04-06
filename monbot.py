import requests  
import os
from flask import Flask, request

DATA_URL = f'{os.environ["DATA_SOURCE"]}'   # add your data source as heroku environment variable

#get report status covid19 by country code
def get_covid19_stats(country="py"):
    response = requests.get(DATA_URL + 'country?countryCode=' + country).json()
    return response[0]

#get report status covid19 for all countries
def get_covid19_global():
    response = requests.get(DATA_URL + 'global').json()
    print(response)
    return response


#get country all code
def get_covid19_contry_code():
    response = requests.get(DATA_URL + 'country').json()
    countryCode = list()
    for i in response:
        countryCode.append(i["countryCode"])
    return countryCode
