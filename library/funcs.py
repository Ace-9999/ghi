import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as dbe

def open_user(user):
	users = get_users_data()
	if users == None:
		users = {}
	if str(user.id) in users:
		return False
	else:
		users[str(user.id)] = {}
		users[str(user.id)]["title"] = f"{user.name}'s TradeShop"
		users[str(user.id)]["about"] = f"Contact {user.mention} to Trade"
		users[str(user.id)]["selling"] = {"lines":["Nothing here yet."]}
		users[str(user.id)]["buying"] = {"lines":["Nothing here yet."]}
		users[str(user.id)]["pcool"] = 0

	dump(users)

	return True

# Fetch the service account key JSON file contents
cred = credentials.Certificate('key.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
'databaseURL': 'https://ghl-shop-storage-default-rtdb.firebaseio.com/'
})

def get_users_data():
	users = dbe.reference('/')

	return users.get()

def dump(users):
	ref = dbe.reference('/')
	ref.set(users)