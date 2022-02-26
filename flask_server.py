import flask
import json, time
import server
import datetime
from server import ALL_USERS_LIST, ALL_USERS
from distance import distance

def update_user_chat():
	global dict_chat_times
	to_delete = []
	for username in dict_chat_times:
		t = time.time()
		if t - dict_chat_times[username] >= 30:
			server.chat.update_friends(username)
			to_delete.append(username)
	for username in to_delete:
		del dict_chat_times[username]

app = flask.Flask(__name__)

@app.route('/<username>/home/',methods=['GET'])
def home_page(username):

	#username = get_username_by_origin() # origin is a comma-sep list of IPs, with the first one hopefully from the device
	update_user_chat()
	data_set = {'Page':'Home','posts':server.get_posts_from_friends(username), #make tthis server.get_posts(username) so that new users
	'Timestamp':str(datetime.datetime.fromtimestamp(time.time()))}
	if len(data_set['posts']) < 5: data_set = { 'Page':'New User Home','posts':server.get_posts() }
	l_posts = [(x["post_no"], x["post_user"]) for x in data_set["posts"]]
	print(f"{data_set['Page']} request response for {username}:",l_posts)
	return data_set

@app.route('/<username>/events_page/',methods=['GET'])
def events_page(username):

	#username = get_username_by_origin() # origin is a comma-sep list of IPs, with the first one hopefully from the device
	update_user_chat()
	data_set = {'Page':'Events','events':server.get_events(username), #make tthis server.get_posts(username) so that new users
	'Timestamp':str(datetime.datetime.fromtimestamp(time.time()))}
	
	return data_set


@app.route('/search/',methods=['GET'])
def search_page():
	user_query = str(flask.request.args.get('q')) #/search/?q=
	data_set = {'Page':'Search','users':server.search_user(user_query),'Timestamp':str(datetime.datetime.fromtimestamp(time.time()))}
	json_string = json.dumps(data_set)
	return json_string

@app.route('/user/<username>',methods=['GET'])
def get_user_page(username):
	return ALL_USERS[username]

@app.route('/<username>/friends/',methods=['GET'])
def friends_page(username):
	friends = server.get_friends(username)
	data_set = {'Page':'Friends', 'users':friends}
	return data_set

@app.route('/<username>/non_friends/',methods=['GET'])
def non_friends_page(username):
	non_friends = server.get_non_friends(username)
	data_set = {'Page':'Non-Friends','users':non_friends}
	return data_set


@app.route('/add_user/',methods=['POST'])
def add_user_page():
	username = flask.request.json['username']
	actual_name = flask.request.json['user_name']

	server.add_user(username,actual_name, '', '', '', '',0,"https://cdn140.picsart.com/297361716279211.png","https://cdn140.picsart.com/297361716279211.png",'')
	server.chat.add_user(username, user_name)

	return flask.jsonify(server.get_posts())

@app.route('/<username>/map/',methods=['GET'])
def map_page(username):
	#update_user_chat()
	global ALL_USERS_LIST, ALL_USERS
	try:
		device_lat = float(str(flask.request.args.get('lat')))
		device_long = float(str(flask.request.args.get('long')))
	except ValueError:
		device_lat = 37.78 #set a default value for San francisco if the phone doesn't request for location automatically
		device_long = -122.44 #happens in Iphone sometimes for God knows why

	location_preference = server.get_location_preference(username)
	if location_preference:
		ALL_USERS_LIST = server.update_location(device_lat, device_long, username)
		ALL_USERS = server.get_all_users()
		#server.update_users()
	else:
		return {'Page':'Map','device_lat':device_lat,'device_long':device_long,'Zoom':15,'Users':[ALL_USERS[username]],'Timestamp':str(datetime.datetime.fromtimestamp(time.time())), "Status":"Location is private",'distances':[],'bypassed':[]}

	data_set = {'Page':'Map','device_lat':device_lat, 'device_long':device_long, 'Zoom':15,'Users':[x for x in ALL_USERS_LIST
									if ((x['username'] == username or x['username'] in ALL_USERS[username]['user_friends'])
									and (x['location_pref0priv1frien2pub'] not in [0,None])
									and x['device_lat'])],'Timestamp':str(datetime.datetime.fromtimestamp(time.time())), "Status":"Successfully updated location",'distances':[],'bypassed':[]}

	for user_ in data_set['Users']:
		if user_['username'] != username:
			data_set['distances'].append( {'username':user_['username'],'distance_from':distance((device_lat, device_long), (user_['device_lat'], user_['device_long']))} )
	for d in data_set['distances']:
		if d['distance_from'] <= 0.3:
			data_set['bypassed'].append(d['username'])
	#add these to the database and inform user of people they recently bypassed
	#l_usrs = [x["username"] for x in data_set["Users"]]
	#print(f"Maps request response for {username}:",l_usrs)
	#print(json.dumps(data_set,indent=3))
	return data_set

@app.route('/signup/',methods=['POST'])
def sign_up():
	main_username = flask.request.json['main_username']
	main_user_name = flask.request.json['main_user_name']
	server.chat.add_user(main_username, main_user_name)
	if main_username not in ALL_USERS:
		server.add_user(main_username, main_user_name,'', '', '', '',0,"https://cdn140.picsart.com/297361716279211.png","https://cdn140.picsart.com/297361716279211.png",'')
		print("Added user", main_username,"to database")
		return {"Page":"Signup","Status":"Success"}
	else:
		return {"Page":"Signup","Status":"User already exists"}



@app.route('/',methods=['POST','GET'])
def login_page():
	username = flask.request.json['main_username']
	#password = flask.request.json['password']
	print("Logging in for",username)
	data_set = {'Page':'Home','main_username':username,'posts':server.get_posts_from_friends(username), #server.get_posts_from_friends(username)
	'Timestamp':str(datetime.datetime.fromtimestamp(time.time()))}
	#json_string = json.dumps(data_set)
	#print("Home request response:",json.dumps(data_set,indent=3))
	return data_set

@app.route('/get-url/<username>/<device_platform>/',methods=['GET'])
def get_chat_url(username, device_platform):
	print("getting chat for ",username)
	return {"Page":"Get Chat URL", "url":f"https://chat_server.../{device_platform}/{username}"}

@app.route('/<username>/post/',methods=['POST'])
def make_post(username):
	update_user_chat()
	# text = flask.request.json['text']
	# time = flask.request.json['time']
	# date = flask.request.json['date']
	# photo = flask.request.json['photo']
	server.add_post(username, flask.request.json)

	return {"Page":"Make post", "status":"success"}

@app.route('/<username>/add_event/',methods=['POST'])
def make_event(username):
	server.add_event(username, flask.request.json)
	return {"Page":"Make event", "status":"success"}


@app.route('/<username>/profile-pic/',methods=['POST'])
def upload_profile_pic(username):
	server.edit_profile_pic(username, flask.request.json)
	return {"Page":"Profile Pic", "status":"success"}


@app.route('/my_info/<username>/',methods=['GET'])
def get_main_user_info(username):
	print("user info gotten,",ALL_USERS[username])
	return ALL_USERS[username]

@app.route('/<username>/make_active/')
def make_active(username):
	return {"state":"active", "active":True}


@app.route('/<username>/make_default/')
def make_default(username):
	return {"state":"default", "active":False}


@app.route('/<username>/chat/')
def chat(username):
	global dict_chat_times
	dict_chat_times[username] = time.time()
	return {"user used chat":1}

@app.route('/<username>/location_set/',methods=['POST'])
def set_location_preference(username):
	status = flask.request.json['location_status']
	status = 0 if "Private" in status else (1 if "Friends" in status else 2)
	server.update_location_preference(username,status)
	return {"page":"set_location_preference","status":"success"}



if __name__ == '__main__':
	app.run(port=7777)



"""
Tell saleh to signup with minerva mail
make chatroom
make map get real time location if user agrees
Make posts by users
"""
