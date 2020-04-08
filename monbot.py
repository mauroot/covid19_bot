import requests  
import os
import matplotlib.pyplot as plt
from datetime import datetime
from flask import Flask, request

DATA_URL = f'{os.environ["DATA_SOURCE"]}'   # add your data source as heroku environment variable
GRAPH_URL = f'{os.environ["DATA_GRAPH"]}'   # add your data source as heroku environment variable

def covid_graph(country="PY"):
    date_end = datetime.today().strftime('%Y-%m-%d')
    date_start = datetime.today().replace(day=1).strftime('%Y-%m-%d')
    response = requests.get(GRAPH_URL + country + '&startDate='+ date_start +'&endDate='+ date_end).json()
    x_list = list()
    y_list = list()
    for i in response:
        dato_x = (datetime.strptime(i["last_updated"], "%Y-%m-%dT%H:%M:%S.%fZ").day)
        x_list.append(dato_x)
        dato_y = i["total_confirmed"]
        y_list.append(dato_y)

    print('aca x:',x_list)
    print('aca y:',y_list)

    # plotting the points 
    plt.plot(x_list, y_list) 

    # naming the x axis 
    plt.xlabel('x - days of month') 
    # naming the y axis 
    plt.ylabel('y - positive cases') 

    # giving a title to my graph 
    plt.title('COVID19 progress for '+ country) 

    # function to show the plot 
    #plt.show()
    #plt.savefig('stats.png')
    #strFile = "./stats.png"
    strFile = os.path.join(app.instance_path, './', 'stats.png')
    
    if os.path.isfile(strFile):
        os.remove(strFile)   #Option: os.system("rm "+strFile)
    plt.savefig(strFile)
    return strFile

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
