import requests
import json
from json2html import *
import random as rand
from flask import Flask, jsonify, request, render_template

from bs4 import BeautifulSoup
import pprint



def is_won(x):
    won = 0
    lost = 0
    total = 0
    draw = 0
    for keys, values in x.items():
        if keys == "matches":
            for item in values:
                
                if item["score"]["winner"] == "HOME_TEAM":
                    won+=1
                elif item["score"]["winner"] == "AWAY_TEAM":
                    lost+=1
                else:
                    draw+=1
    
        

            
    print(won)
    print(lost)
    print(total)
    dic = {"result":  "score", "won": won, "lost": lost}
    return dic


def standling_table():
    standing = standings["standings"]
    for val in standing:
        
        if (val["type"] == "TOTAL"):
            l = val["table"]
    
    for i in list(l[0]["team"]):
        for j in range(len(l)):
            if i=="name":
                l[j]["team"]=l[j]["team"][i]
                
    pprint.pprint(l)
    st=json2html.convert(json=l)
    soup=BeautifulSoup(st, 'html.parser')
    soup.find('table')['class'] = 'table'
    soup.find('thead')['class'] = 'table-dark'
    return soup


def score_calculate_home(team_name, away_team, x):
    
    for keys, values in x.items():
        if keys == "matches":
            for item in values:
                if item["homeTeam"]["name"] == team_name and item["awayTeam"]["name"] == away_team:
                    try:
                        home_score = int(item['score']['fullTime']['home'])
                        away_score = int(item['score']['fullTime']['away'])
                        difference = home_score - away_score
                        return difference
                    except:
                        continue

                

 
def gd_tracker(x):
    gd = {}
    lst = []
    for keys, values in x.items():
        if keys == "matches":
            for item in values:
                if item["homeTeam"]["name"]not in gd:
                    goal_difference = score_calculate_home(item["homeTeam"]["name"],item["awayTeam"]["name"],x)
                    gd[item["homeTeam"]["name"]] = [goal_difference]
                else:
                    goal_difference = score_calculate_home(item["homeTeam"]["name"],item["awayTeam"]["name"],x)
                    gd[item["homeTeam"]["name"]].append(goal_difference)
    return gd
                    
                # else:
                    
                    # goal_difference = score_calculate_home(item["homeTeam"]["name"], item["awayTeam"]["name"], x)
                    # # if goal_difference != None:
                    # lst[item["homeTeam"]["name"]] = {item["awayTeam"]["name"]: goal_difference}
                    # gd[item["homeTeam"]["name"]] = lst
    # return gd
                    
def total_matches(x):
    match_tracker = {}
    for keys, values in x.items():
        if keys == "matches":
            for item in values:

                if item["homeTeam"]["name"]not in match_tracker:
                    
                    
                    match_tracker[item["homeTeam"]["name"]] =1
                else:
                    match_tracker[item["homeTeam"]["name"]]+=1
                
                
                if item["awayTeam"]["name"] not in match_tracker:
                    match_tracker[item["awayTeam"]["name"]] = 1
                
                else:
                    match_tracker[item["awayTeam"]["name"]] +=1
            
    return match_tracker

# def gd_tracker(){
#     gd = {}
#     for keys, values in x.items():
#         if keys == "matches":
#             for item in values:
#                  if item["homeTeam"]["name"]not in match_tracker:
                    
    
# }
    


url = "https://api.football-data.org/v4/competitions/PL/matches"
url_standlings= "http://api.football-data.org/v4/competitions/PL/standings"
# querystring = {"market": "classic",
#                "iso_date": "2018-12-01", "federation": "UEFA"}

headers = {
    # "X-RapidAPI-Key": "44a7105103msh2ecaa0f17a01cc3p18e657jsn08369d44ec46",
    "X-Unfold-Goals": "true",
    "X-Auth-Token": "a7067544d5094388bad228ab62cbda25"
    
    # "X-RapidAPI-Host": "football-prediction-api.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)
result = response.json()
standings = requests.request("GET", url_standlings, headers=headers).json()
gdx = requests.request("GET",url+"?season=2020", headers=headers).json()
file = open("data2.json", "w")
# x = file.read()
# print(result)
json.dump(result, file, indent=4)
# result = json.loads(x)

# print(soup.prettify())
# file2 = open("data3.html", "w")
# file2.write(soup.prettify())
app = Flask(__name__)

@app.route("/")
def view_home():
    
    return render_template("index.html", title="Analytics Website")

@app.route("/pie")
def index():
    # return "<h1>hi</h1>"
    # data = {'Task' : 'Hours per Day', 'Work' : 11, 'Eat' : 2, 'Commute' : 2, 'Watching TV' : 2, 'Sleeping' : 7}
	#print(data)
    
    data = is_won(result)
    
    return render_template('pie-chart.html', data=data, title="Full Match Analytics")
    # return render_template('pie-chart.html', data=data)
    # return data
    # return x
    # print(x)
@app.route("/matches")
def inex():
    data = total_matches(result)
    return data

@app.route("/standings")
def table():
    p = standling_table()
    return render_template("record.html",table=p,title="Standings")
    # print(response.text)

@app.route("/gd")
def gd():
    g = gd_tracker(gdx)
    d = {}
    d["Arsenal FC"] =g["Arsenal FC"]
    # return g
    return render_template('line_chart.html', data=d,title="Match Analytics")

@app.route("/g")
def jd():
    g = gd_tracker(gdx)
    d = {}
    d["Manchester City FC"] =g["Manchester City FC"]

    # return g
    return render_template('line_chart_manC.html', data=d,title="Match Analytics")


    
if __name__ == "__main__":
    app.run()