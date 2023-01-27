import ast
import json
import os
import keyring
import pickle
import argparse
import requests
import webbrowser
from fuzzywuzzy import process
#from dotenv import load_dotenv
#load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument('--search', help='search sites for')
parser.add_argument('--run', help='run an application')
parser.add_argument('--steamid', help='Set steam id (only needed once)')
parser.add_argument('--steamkey', help='Set steam api key (only needed once)')
parser.add_argument('--type', help='run an application', default="run", type=str)
parser.add_argument('--num', help='how many results?', default=10, type=int)
args = parser.parse_args()

if args.steamid:
	keyring.set_password("system", "STEAM_PROFILE_ID", args.steamid)

if args.steamkey:
	keyring.set_password("system", "STEAMAPI_KEY", args.steamkey)

if args.search:
	if not os.path.isfile("steam.pickle"):
		devApiKey = keyring.get_password("system", "STEAMAPI_KEY")
		profileId = keyring.get_password("system", "STEAM_PROFILE_ID")
		if devApiKey == None or profileId == None:
			print("Need to set STEAMAPI_KEY and STEAM_PROFILE_ID (python plugin_steam.py --steamid <id> --steamkey <key>)")
			exit(1)
		steam_dict = {}

		response = requests.get(f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={devApiKey}&steamid={profileId}&format=json&include_appinfo=1)")
		if response.status_code == 200:
			data = response.json()
			#print(data)
			for game in data['response']['games']:
				steam_dict[game['name']] = game['appid']

		else:
			print("Error getting steam games")
			exit(1)

		with open("steam.pickle", "wb") as f:
			pickle.dump(steam_dict, f)

	with open("steam.pickle", "rb") as f:
		steam_dict = pickle.load(f)

	new_steam_obj = []
	#print(steam_dict)

	results = process.extract(args.search, steam_dict.keys(), limit=args.num)
	for result in results:
		obj = {}
		obj['name'] = result[0]
		obj['action'] = steam_dict[result[0]]
		obj['confidence'] = result[1]
		obj['description'] = ""
		new_steam_obj.append(obj)
	print( json.dumps(new_steam_obj) )

if args.run:
	#https://developer.valvesoftware.com/wiki/Steam_browser_protocol
	webbrowser.open(f"steam://{args.type}/{args.run}")