from flask import Flask, jsonify, request #import objects from the Flask model
from flask_cors import CORS
import threading
import requests
import os

app = Flask(__name__) #define app using Flask
CORS(app)

def setData(allData):
    global globalData
    globalData = []
    data = []
    tempActive = 0
    tempConfirmed = 0
    tempDeaths = 0
    tempRecovered = 0
    length = len(allData) 
    for i in range(length): 
        if allData[i]['Province'] == '' and allData[i]['Country'] != 'China':
            data.append(allData[i])
        elif allData[i]['Country'] == 'China' or allData[i]['Country'] == 'Australia':
            if allData[i]['Date'] != allData[i+1]['Date']:
                tempActive = tempActive + allData[i]['Active']
                tempConfirmed = tempConfirmed + allData[i]['Confirmed']
                tempDeaths = tempDeaths + allData[i]['Deaths']
                tempRecovered = tempRecovered + allData[i]['Recovered']
                tempObj = {}
                tempObj = {"Country": allData[i]['Country'],
                "CountryCode": allData[i]['CountryCode'],
                "Province": "",
                "City": "",
                "CityCode": "",
                "Lat": "",
                "Lon": "",
                "Confirmed": tempConfirmed,
                "Deaths": tempDeaths,
                "Recovered": tempRecovered,
                "Active": tempActive,
                "Date": allData[i]['Date']}
                data.append(tempObj)
                tempActive = 0
                tempConfirmed = 0
                tempDeaths = 0
                tempRecovered = 0
            elif allData[i]['Date'] == allData[i+1]['Date']:
                tempActive = tempActive + allData[i]['Active']
                tempConfirmed = tempConfirmed + allData[i]['Confirmed']
                tempDeaths = tempDeaths + allData[i]['Deaths']
                tempRecovered = tempRecovered + allData[i]['Recovered']
    globalData = data

def myApiCall():
    url = ('https://api.covid19api.com/all')
    response = requests.get(url)
    response = response.json()
    setData(response)
    test = "Getting data from external API"
    print(test)
    threading.Timer(600, myApiCall).start()
myApiCall()

@app.route('/allData/', methods=['GET'])
def all():
    global globalData
    return jsonify(globalData)

@app.route('/news/', methods=['GET'])
def getCountryNews():
    param = {}
    param = request.args.to_dict()
    country = param["queryCountry"]
    url = ('http://newsapi.org/v2/top-headlines?q=COVID-19&country='+country+'&apiKey=940263c7c37248af8b1f276dc8843634')
    response = requests.get(url)
    return response.json()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
	app.run(debug=True, host='0.0.0.0', port=port) #run app on port 8080 in debug mode
