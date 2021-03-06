import requests  
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from flask import Flask, request

DATA_URL = f'{os.environ["DATA_SOURCE"]}'   # add your data source as heroku environment variable
GRAPH_URL = f'{os.environ["DATA_GRAPH"]}'   # add your data source as heroku environment variable
SEND_GRAPH_URL = f'{os.environ["SEND_GRAPH"]}'   # add your data source as heroku environment variable

def y_formatter(y, pos):
    return str(f'{int(y):,}').replace(',', '.')

def covid_graph(country="PY"):
    plt.clf()    
    date_end = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    #date_end = datetime.today().strftime('%Y-%m-%d')
    date_start = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    response = requests.get(GRAPH_URL + country + '&startDate='+ date_start +'&endDate='+ date_end).json()
    days_list = list()
    confirm_list = list()
    death_list = list()
    recovered_list = list()    
    for i in response:
        dato_x = (str((datetime.strptime(i["last_updated"], "%Y-%m-%dT%H:%M:%S.%fZ").day))+"-"+str((datetime.strptime(i["last_updated"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%b"))))
        days_list.append(dato_x)
        dato_y1 = i["total_confirmed"]
        confirm_list.append(dato_y1)
        dato_y2 = i["total_deaths"]
        death_list.append(dato_y2)
        dato_y3 = i["total_recovered"]
        recovered_list.append(dato_y3)
        
    y_group = [death_list,confirm_list]
    plt.style.use('dark_background')
        
    ax = plt.gca()
    locator = mdates.DayLocator()
    ax.yaxis.grid(alpha=0.2)
    ax.xaxis.set_major_locator(locator)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(y_formatter))
    ax.yaxis.set_major_locator(plt.MaxNLocator(10))
    
    # plotting the points secuential mode
    #plt.plot(days_list, recovered_list,'k',linewidth=0, color='#ADE900', label=y_formatter(max(recovered_list),0)+' '+'Recovered', alpha=0.8) 
    #plt.plot(days_list, confirm_list,'k', linewidth=0, color='blue', label=y_formatter(max(confirm_list),0)+' '+'Positives', alpha=0.8) 
    #plt.plot(days_list, death_list,'k', linewidth=0, color='#EB1B4C', label=y_formatter(max(death_list),0)+' '+'Deaths', alpha=0.8) 
    #plt.stackplot(days_list,y_group, labels=[y_formatter(max(death_list),0)+' '+'Deaths',y_formatter(max(confirm_list),0)+' '+'Positives'], colors=['#EB1B4C','blue'], alpha=0.8 )

    #plt.fill_between(days_list, confirm_list, color='blue',alpha=0.8)
    #plt.fill_between(days_list, death_list, color='#EB1B4C',alpha=0.8)
    #plt.fill_between(days_list, recovered_list, color='green',alpha=0.8)
       
    #alpha = 1.0 #optional for set autodecrement alpha property
    # plotting the points auto sort mode
    for layer in sorted([(max(recovered_list),"recovered_list","#ADE900","Recovered"),(max(confirm_list),"confirm_list","blue","Positives"),(max(death_list),"death_list","#EB1B4C","Deaths")], reverse=True):
    #    alpha-=0.13 #decrement alpha property
        plt.plot(days_list, eval(layer[1]),'k',linewidth=0, color=layer[2], label=y_formatter(max(eval(layer[1])),0)+' '+layer[3], alpha=0.8)     
        plt.fill_between(days_list, eval(layer[1]), color=layer[2],alpha=0.8)

    #enable and position legend
    #plt.legend() 
    leg = plt.legend(borderpad=1)
    # get the lines and texts inside legend box
    leg_lines = leg.get_lines()
    leg_texts = leg.get_texts()
    # bulk-set the properties of all lines and texts
    plt.setp(leg_lines, linewidth=6)
    plt.setp(leg_texts, fontsize='medium')
    plt.xticks(days_list,rotation=75,fontsize=8)
    
    # naming the x axis 
    plt.xlabel('x - Days') 
    # naming the y axis 
    plt.ylabel('y - Persons') 

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
    for spine in plt.gca().spines.values():
       spine.set_visible(False)
    
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
