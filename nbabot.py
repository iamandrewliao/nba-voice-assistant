import numpy as np
import pandas as pd

from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import playercareerstats

import speech_recognition as sr
import pyttsx3

import datetime

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		audio = r.listen(source)
		said = ""
		try:
			said = r.recognize_google(audio)
			print(said)
		except Exception as e:
			print('Exception: ' + str(e))
	return said

def get_player_stats(name, season):
	nba_players = players.get_players()
	try:
		player = [player for player in nba_players if player['last_name'] == name or player['first_name'] == name or player['full_name']== name][0]
	except:
		print('Invalid name')
		return
	career = playercareerstats.PlayerCareerStats(player_id=player['id'])
	career_df = career.get_data_frames()[0]
	print(career_df[career_df['SEASON_ID']==season].iloc[:, 4:])

# Getting player data is by audio (saying the name and season).
# Speech recognition can be inaccurate and may not recognize uncommon player names. 
# To reduce the chance of error, I've made it so it will also work with the player's last name or first name only.
# However, this means no one else can have had the same last name or the same first name.
def stats_by_speech():
	speak("Give me an NBA player's last name or first name")
	name = get_audio()
	nba_players = players.get_players()
	try:
		player = [player for player in nba_players if player['last_name'] == name or player['first_name'] == name or player['full_name']== name][0]
	except:
		print('Invalid name')
		return
	speak("Now give me the year in question")
	try:
		year = get_audio()
		season = f"{int(year)}-{str(int(year)+1)[-2:]}"
	except:
		print('Invalid year')
		return
	get_player_stats(name, season)

#get_player_stats('Harden', '2018-19')
stats_by_speech()