import requests
import argparse
import sqlite3
import sys


user = '' 		# Fill this with your name/email
password = ''	# Fill this with your password
save_slot = 1 			# Select a save slot (1, 2 or 3)

url = 'https://ptd1.jordanplayz158.xyz/php/newPoke8.php'

# Loads the database required to query moves and abilities
conn = sqlite3.connect('poke_data.db')
cursor = conn.cursor()

# This variable stores the login response parameters
user_data = {}
default_moves = [0, 0, 0, 0]


def main():

	# Login into your account and save the data.
	login()

	# Uses argparse to create the CLI
	parser = argparse.ArgumentParser(description="CLI Account Editor for PTD.")
	egroup = parser.add_mutually_exclusive_group()

	# All the argparse commands
	parser.add_argument('-a', '--add', help='Adds a pokemon to your account.', metavar='', nargs='+')
	parser.add_argument('-l', '--level', type=int, help='Defines the level of your pokemon.', metavar='', default=100)
	egroup.add_argument("-s", "--shiny", action="store_true", help='Set your pokemon as a shiny.', default=0)
	egroup.add_argument("-ss", "--shadow", action="store_true", help='Set your pokemon as a shadow.', default=0)
	parser.add_argument('-m', '--money', type=int, help='Defines the amount of money.', metavar='', default=user_data[f'Money{save_slot}'])
	parser.add_argument('-m1', '--move1', help='Defines pokemon first move.', metavar='', default='0')
	parser.add_argument('-m2', '--move2', help='Defines pokemon second move.', metavar='', default='0')
	parser.add_argument('-m3', '--move3', help='Defines pokemon third move.', metavar='', default='0')
	parser.add_argument('-m4', '--move4', help='Defines pokemon fourth move.', metavar='', default='0')
	parser.add_argument('-v', '--version', help='Changes game version (Red/Blue).', choices=['Blue', 'Red'], default=user_data[f'Version{save_slot}'])
	parser.add_argument('-n', '--nickname', help='Changes nickname of the current save.', metavar='', default=user_data[f'Nickname{save_slot}'])
	parser.add_argument('-b', '--badges', type=int, help='Change the number of badges.', metavar='', default=user_data[f'Badges{save_slot}'])
	parser.add_argument('--unlockchallenges', help='Unlocks all challenges.', action='store_true', default=user_data[f'Challenge{save_slot}'])
	parser.add_argument('--unlockdex', help='Unlocks all entrys in pokedex.', action='store_true', default=user_data[f'Nickname{save_slot}'])
	parser.add_argument('--unlocklevels', help='Unlocks all levels.', action='store_true', default=user_data[f'Classic{save_slot}'])

	args = parser.parse_args()

	# Save account with the modified data
	save(args)


def login():

	login_data = {
		'Email': user,
		'Pass': password,
		'ver': '750',
		'Action': 'loadAccount'
	}

	# Gets the response of the post method and split every return parameter
	try:
		login_response = requests.post(url, login_data)
		login_response = login_response.text.split('&')
	except:
		sys.exit('Could not connect to the server, check url.')

	# Turns each parameter into a dictionary
	for i in login_response:
		i = i.split('=')
		user_data[i[0]] = i[1]

	if (user_data['Result']) == 'Failure':
		print(f"Error: {user_data['Reason']}")
		sys.exit('Check your login details.')


def save(args):

	if (args.unlockchallenges == True):
		user_data[f'Challenge{save_slot}'] = 5

	if (args.unlocklevels == True):
		user_data[f'Advanced{save_slot}'] = 41

	# The pokedex is sent to the server as a sequence of 151 numbers,
	# 0 or 1 depending if you have the pokemon
	if (args.unlockdex == True):
		user_data[f'dex{save_slot}'] = '1'*151
		user_data[f'dex{save_slot}Shiny'] = '1'*151
		user_data[f'dex{save_slot}Shadow'] = '1'*151

	match (args.version):
		case 'Red':
			user_data[f'Version{save_slot}'] = 1
		case 'Blue':
			user_data[f'Version{save_slot}'] = 2

	save_string = (
	f"currentSave={user_data['CurrentSave']}&"
	f"whichProfile={save_slot}&"
	f"badges={args.badges}&"
	f"myTID=0&"
	f"challenge={user_data[f'Challenge{save_slot}']}&"
	f"a_story={user_data[f'Advanced{save_slot}']}&"
	f"a_story_a={user_data[f'Advanced{save_slot}_a']}&"
	f"c_story={user_data[f'Classic{save_slot}']}&"
	f"c_story_a={user_data[f'Classic{save_slot}_a']}&"
	f"NPCTrade={user_data[f'NPCTrade{save_slot}']}&"
	f"ShinyHunt={user_data[f'shinyHunt{save_slot}']}&"
	f"Money={args.money}&"
	f"Nickname={args.nickname}&"
	f"myVID=0&"
	f"Version={user_data[f'Version{save_slot}']}&"
	f"Avatar={user_data[f'avatar{save_slot}']}&"
	f"HMI={user_data[f'HMI{save_slot}']}&"
	f"dex1={user_data['dex1']}&"
	f"dex1Shiny={user_data['dex1Shiny']}&"
	f"dex1Shadow={user_data['dex1Shadow']}&"
	)

	addpoke, errors = add_poke(args)

	save_data = {
		'Email': user,
		'Pass': password,
		'ver': '750',
		'Action': 'saveAccount',
		# HMP is How Many Pokemon to add, discounted errors case user writes a wrong ID or pokemon name.
		'saveString': save_string + f"HMP={len(args.add) - errors}&" + addpoke
	}

	#print(save_data)
	save_response = requests.post(url, save_data)
	save_response = save_response.text.split('&')
	
	print(save_response[0])


def add_poke(args):

	errors = 0
	addpoke = ''

	# If no add argument is passed creates a empty list, just so the len() function in HMP returns 0.
	if (args.add == None):
		args.add = []
	else:
		for arg in args.add:
			# Filter user input so it will match the database
			arg = arg.lower().capitalize().strip(',')

			# Save pokemon default moves from the database into a moveset variable
			moveset = cursor.execute(f"SELECT move1, move2, move3, move4 FROM pokemon WHERE name = '{arg}'")
			# Loop through all 4 moves and add to the request, if None return 0
			for move in moveset:
				for move_name in range(4):
					ids = cursor.execute(f"SELECT id FROM moves WHERE name = '{move[move_name]}'")
					check = ids.fetchone()

		# Filter user input so it will match the database
		for filter in range(len(args.add)):
			args.add[filter] = args.add[filter].lower().capitalize().strip(',')

			# Checks if the input given is and id or poke name - True if ID False if Pokename
			if bool(cursor.execute(f"SELECT name FROM pokemon WHERE id='{args.add[filter]}'").fetchone()):
				args.add[filter] = cursor.execute(f"SELECT name FROM pokemon WHERE id='{args.add[filter]}'").fetchone()[0]

		# Creates the pokemon default moveset
		i = 1

		for arg in args.add:

			create_moveset(args, arg)

			# Data that is sent through the request when you use --add
			try:
				poke_num = cursor.execute(f"SELECT id FROM pokemon WHERE name = '{arg}'")

				addpoke += (
					f"poke{i}_reason=cap&"
					f"poke{i}_num={poke_num.fetchone()[0]}&"
					f"poke{i}_nickname={arg}&"
					f"poke{i}_exp=0&"
					f"poke{i}_lvl={args.level}&"
					f"poke{i}_m1={default_moves[0]}&"
					f"poke{i}_m2={default_moves[1]}&"
					f"poke{i}_m3={default_moves[2]}&"
					f"poke{i}_m4={default_moves[3]}&"
					f"poke{i}_ability=0&"
					f"poke{i}_mSel=1&"
					f"poke{i}_targetType=1&"
					f"poke{i}_tag=n&"
					f"poke{i}_item=0&"
					f"poke{i}_owner=0&"
					f"poke{i}_myID=0&"
					f"poke{i}_pos=1&"
					f"poke{i}_extra={(args.shiny * 151) + (args.shadow * 555)}&"
				)

				if (args.shiny):
					extra = ' Shiny '
				elif (args.shadow):
					extra = ' Shadow '
				else:
					extra = ' '

				print(f'Added Lvl. {args.level}{extra}{arg} to your account!\n')

				i += 1
			except:
				errors += 1

				print(f"Error adding pokemon: '{arg}' doesn't exist...\n")

	return addpoke, errors


def create_moveset(args, arg):

	# Defines the pokemon moves
	move_args = [args.move1, args.move2, args.move3, args.move4]
	for move in range(len(move_args)):
		move_args[move] = move_args[move].lower().capitalize()
		if bool(cursor.execute(f"SELECT name FROM moves WHERE id='{move_args[move]}'").fetchone()):
			move_args[move] = cursor.execute(f"SELECT name FROM moves WHERE id='{move_args[move]}' LIMIT 1").fetchone()[0]

	# Save pokemon default moves from the database into a moveset variable
	moveset = cursor.execute(f"SELECT move1, move2, move3, move4 FROM pokemon WHERE name = '{arg}'")

	# Loop through all 4 moves and add to the request, if None return 0
	for move in moveset:
		for id in range(4):
			ids = cursor.execute(f"SELECT id FROM moves WHERE name = '{move[id]}' LIMIT 1")
			check = ids.fetchone()
			if check != None:
				default_moves[id] = check[0]
			else:
				default_moves[id] = 0

	# Pass each move passed via args.move to the pokemon, if it doesn't exist, return 0 as move.
	for ma in range(4):
		try:
			if (move_args[ma] != '0'):
				default_moves[ma] = cursor.execute(f"SELECT id FROM moves WHERE name = '{move_args[ma]}'").fetchone()[0]
				print(f"Added move {move_args[ma]} as Move {ma+1} for {arg}.")
		except:
			default_moves[ma] = 0
			print(f"Error: Move {move_args[ma]} doesn't exist.")
	print()


if __name__ == "__main__":
    main()
