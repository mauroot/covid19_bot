import requests
import os
from datetime import datetime
from flask import Flask, request
from monbot import get_covid19_stats, get_covid19_global, get_covid19_contry_code, covid_graph

BOT_URL = f'https://api.telegram.org/bot{os.environ["BOT_KEY"]}/' 

app = Flask(__name__,static_url_path='', static_folder='img')

@app.route('/', methods=['POST'])
   
def main():
    #emoji set unicode
    sick_active = u'\U0001F637'
    sick_confirm = u'\U0001F912'
    sick_dialy = u'\U0001F927'
    death_dialy = u'\U0001F480'
    death_total = u'\U00002620'
    recovered = u'\U0001F601'
    updated = u'\U0001F916'
   
    data = request.json
    country_check = get_covid19_contry_code()

    chat_id = data['message']['chat']['id']
    message = data['message']['text']

    if message.lower() in ["hi","hello","/start"]:
        message_send = "Hello Welcome to our bot. Type Country Code like 'us' to USA."
    elif message.lower() in ["/help"]:
        message_send = "Hi, to know stats for advance of coronavirus in a specific country type the country code like 'us' to USA or 'fr' to FRANCE.\nFor know the global stats type 'global'."
    elif message.lower() == "global":
        stats = get_covid19_global()
        message_send = "*The stats for all countrys is:*\n" + sick_confirm + " Total confirmed cases: *"+ str(f'{stats["totalConfirmed"]:,}').replace(',', '.') + "*\n" + death_total + " Total Deaths: *" + str(f'{stats["totalDeaths"]:,}').replace(',', '.') + "*\n" + recovered + " Total Recovered: *" + str(f'{stats["totalRecovered"]:,}').replace(',', '.') + "*\n" + sick_active + " Total Active Cases: *" + str(f'{stats["totalActiveCases"]:,}').replace(',', '.') + "*\n" + sick_dialy + " Total New Cases: *" + str(f'{stats["totalNewCases"]:,}').replace(',', '.') + "*\n" + death_dialy + " Total New Deaths: *" + str(f'{stats["totalNewDeaths"]:,}').replace(',', '.')+ "*\n" + updated + " Updated: " + str(datetime.strptime(stats["created"], "%Y-%m-%dT%H:%M:%S.%fZ").date()) + " " + str(datetime.strptime(stats["created"], "%Y-%m-%dT%H:%M:%S.%fZ").time())     
    elif message.upper() in country_check:
        stats = get_covid19_stats(message.upper())
        message_send = "*The stats for " + stats["country"] + " is:*\n" + sick_confirm + " Total confirmed cases: *"+ str(f'{stats["totalConfirmed"]:,}').replace(',', '.') + "*\n" + death_total + " Total Deaths: *" + str(f'{stats["totalDeaths"]:,}').replace(',', '.') + "*\n" + recovered + " Total Recovered: *" + str(f'{stats["totalRecovered"]:,}').replace(',', '.') + "*\n" + sick_active + " Active Cases: *" + str(f'{stats["activeCases"]:,}').replace(',', '.') + "*\n" + sick_dialy + " Daily Confirmed: *" + str(f'{stats["dailyConfirmed"]:,}').replace(',', '.') + "*\n" + death_dialy + " Daily Deaths: *" + str(f'{stats["dailyDeaths"]:,}').replace(',', '.') + "*\n" + updated + " Updated: " + str(datetime.strptime(stats["lastUpdated"], "%Y-%m-%dT%H:%M:%S.%fZ").date()) + " " + str(datetime.strptime(stats["lastUpdated"], "%Y-%m-%dT%H:%M:%S.%fZ").time())
        graph = covid_graph(message.upper())
    else:
        message_send = "Sorry not understand what you say, try again a country code like 'py' for Paraguay"

    json_data = {
        "chat_id": chat_id,
        "parse_mode": "Markdown",
        "text": message_send,
    }

    json_graph = {
        "chat_id": chat_id,
        "photo" : "https://telegram.org/img/t_logo.png", #graph,
        "caption" : "Graph Stats for Positive Cases",
    }                                                                                                                          

    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=json_data)

    photo_url = BOT_URL + 'sendPhoto'
    requests.post(photo_url, json=json_graph)
    
    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)),debug=True, use_reloader=True)
