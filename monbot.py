import requests  
import os
import matplotlib.pyplot as plt
from datetime import datetime
from flask import Flask, request

DATA_URL = f'{os.environ["DATA_SOURCE"]}'   # add your data source as heroku environment variable
GRAPH_URL = f'{os.environ["DATA_GRAPH"]}'   # add your data source as heroku environment variable
SEND_GRAPH_URL = f'{os.environ["SEND_GRAPH"]}'   # add your data source as heroku environment variable

def y_formatter(y, pos):
    return str(f'{int(y):,}').replace(',', '.')

def covid_graph(country="PY"):
    plt.clf()    
    date_end = datetime.today().strftime('%Y-%m-%d')
    date_start = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    response = requests.get(GRAPH_URL + country + '&startDate='+ date_start +'&endDate='+ date_end).json()
    days_list = list()
    confirm_list = list()
    death_list = list()
    for i in response:
        dato_x = (str((datetime.strptime(i["last_updated"], "%Y-%m-%dT%H:%M:%S.%fZ").day))+"-"+str((datetime.strptime(i["last_updated"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%b"))))
        days_list.append(dato_x)
        dato_y1 = i["total_confirmed"]
        confirm_list.append(dato_y1)
        dato_y2 = i["total_deaths"]
        death_list.append(dato_y2)
        
    ax = plt.gca()
    locator = mdates.DayLocator()
    ax.yaxis.grid(alpha=0.2)
    ax.xaxis.set_major_locator(locator)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(y_formatter))
    ax.yaxis.set_major_locator(plt.MaxNLocator(20))
    
    # plotting the points 
    plt.plot(days_list, confirm_list,'k', color='blue',label=y_formatter(max(confirm_list),0)+' '+'Positives') 
    plt.plot(days_list, death_list,'k', color='red', label=y_formatter(max(death_list),0)+' '+'Deaths') 

    plt.xticks(days_list,rotation=75,fontsize=8)

    plt.legend()    
    
    # naming the x axis 
    plt.xlabel('x - days of month') 
    # naming the y axis 
    plt.ylabel('y - positive cases') 

    # giving a title to my graph 
    plt.title('COVID19 progress for '+ response[0]['country']) 

    # function to show the plot 
    #plt.show()
    strFile = "static/"+datetime.today().strftime("%Y%m%d-%H%M%S")+".png"
    graphFile = SEND_GRAPH_URL + strFile
    print(graphFile)
    
    folder = os.path.dirname(os.path.abspath(__file__))+'/static'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    plt.tight_layout()
    plt.savefig(strFile)
    return graphFile

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
