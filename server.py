import setup_postgres
import places_api as P
import requests

def get_all_users_list():
	code = "SELECT * FROM users"
	with setup_postgres.connect() as connect:
		if connect:
			conn, cur = connect
			cur.execute(code)
			return_list = [dict(x) for x in cur.fetchall()]
			for user_dict in return_list:
				# if user_dict["user_location"]:
				# 	user_technical_location = P.place_list(user_dict['user_location'])[0]
				# 	user_dict["lat"] = user_technical_location.lat
				# 	user_dict["long"] = user_technical_location.long
				if user_dict["user_events"] not in [None, ''] and int(user_dict["user_events"]) > 0:
					cur.execute("SELECT * FROM events WHERE event_no = %s", (user_dict["user_events"],))
					event = cur.fetchall()
					user_dict["user_events"] = dict(event[0])
				if not user_dict["user_small_photo"]:
					user_dict["user_small_photo"] = "https://cdn140.picsart.com/297361716279211.png"
					user_dict["user_large_photo"] = "https://cdn140.picsart.com/297361716279211.png"
				if not user_dict['user_ip']: user_dict['user_ip'] = '';
				if not user_dict['user_location']: user_dict['user_location'] = '';
				if not user_dict['user_bio']: user_dict['user_bio'] = '';
				if not user_dict['user_extra_bio']: user_dict['user_extra_bio'] = '';
				if not user_dict['user_friends']: user_dict['user_friends'] = '';
				if not user_dict['user_events']: user_dict['user_events'] = '';
			return return_list

ALL_USERS_LIST = get_all_users_list()

def get_all_users():
	return_dict = dict()
	for user_dict in ALL_USERS_LIST:
		return_dict[user_dict["username"]] = user_dict
	return return_dict

ALL_USERS = get_all_users()

def get_posts():
	with setup_postgres.connect() as connect:
		if connect:
			conn, cur = connect
			cur.execute("SELECT * FROM posts")
			return_list = [dict(x) for x in cur.fetchall()]

			for post_dict in return_list:
				poster_username = post_dict["post_user"]
				post_dict["post_user"] = ALL_USERS[poster_username]
				post_dict['post_text'] = post_dict['post_text'].replace('$COM',',')
				if post_dict['post_media']:
					post_dict['has_media'] = True
				else:
					post_dict['has_media'] = False
			return return_list

def get_events(username):
	with setup_postgres.connect() as connect:
		if connect:
			conn, cur = connect
			print("connected")
			cur.execute("SELECT * FROM events")
			return_list = [dict(x) for x in cur.fetchall()]

			for post_dict in return_list:
				poster_username = post_dict["user_posted"]
				post_dict["user_posted"] = ALL_USERS[poster_username]
				post_dict['event_description'] = post_dict['event_description'].replace('$COM',',')
				if post_dict['event_media']:
					post_dict['has_media'] = True
				else:
					post_dict['has_media'] = False
			return return_list

def get_friends(username):
	with setup_postgres.connect() as connect:
		if connect:
			return_list = []
			conn, cur = connect
			user_friends = ALL_USERS[username]["user_friends"]
			for usern in ALL_USERS:
				if usern in user_friends:
					return_list.append(ALL_USERS[usern].copy())
			l = [x["username"] for x in return_list]
			print("get_friends will return",l,"for",username)
			return return_list


def get_non_friends(username):
	with setup_postgres.connect() as connect:
		if connect:
			return_list = []
			conn, cur = connect
			user_friends = ALL_USERS[username]["user_friends"]
			for usern in ALL_USERS:
				if not(usern in user_friends) and usern != username:
					return_list.append(ALL_USERS[usern].copy())
			l = [x["username"] for x in return_list]
			print("get_non_friends will return",l,"for",username)
			return return_list

def get_posts_from_friends(username):
	with setup_postgres.connect() as connect:
		if connect:
			conn, cur = connect
			user_friends = ALL_USERS[username]["user_friends"]
			cur.execute("SELECT * FROM posts WHERE (position(post_user in %s)>0) or post_user = %s", (user_friends,username)) #check if post_user is a substring of user_friends
			return_list = [dict(x) for x in cur.fetchall()]
			print("get_posts_from_friends will return",return_list,"for",username)
			for post_dict in return_list:
				poster_username = post_dict["post_user"]
				post_dict["post_user"] = ALL_USERS[poster_username]
				post_dict["post_text"] = post_dict["post_text"].replace('$COM',',')
				if post_dict['post_media']:
						post_dict['has_media'] = True
				else:
					post_dict['has_media'] = False
			return return_list

def search_user(query):
	"""Should update this function, and all functions to accomodate dynamic user list"""
	#cur.execute("SELECT * FROM users WHERE position(%s, username)>0 || position(%s, user_name)>0", (query,))
	return_list = []
	for username in ALL_USERS:
		if query in username or query in ALL_USERS[username]["user_name"]:
			return_list.append(ALL_USERS[username])
	return return_list

def update_location(device_lat, device_long, username):
	with setup_postgres.connect() as connect:
		if connect:
			conn, cur = connect
			code = "UPDATE users SET device_lat = %s, device_long = %s WHERE username = %s"
			cur.execute(code, (device_lat, device_long, username))
			cur.execute("SELECT * FROM users")
			return_list = [dict(x) for x in cur.fetchall()]
			for user_dict in return_list:
				# if user_dict["user_location"]:
				# 	...
				# 	user_technical_location = P.place_list(user_dict['user_location'])[0]
				# 	user_dict["lat"] = user_technical_location.lat
				# 	user_dict["long"] = user_technical_location.long
				if user_dict["user_events"] not in [None, ''] and int(user_dict["user_events"]) > 0:
					cur.execute("SELECT * FROM events WHERE event_no = %s", (user_dict["user_events"],))
					event = cur.fetchall()
					user_dict["user_events"] = dict(event[0])
				if not user_dict['user_ip']: user_dict['user_ip'] = '';
				if not user_dict['user_location']: user_dict['user_location'] = '';
				if not user_dict['user_bio']: user_dict['user_bio'] = '';
				if not user_dict['user_extra_bio']: user_dict['user_extra_bio'] = '';
				if not user_dict['user_friends']: user_dict['user_friends'] = '';
				if not user_dict['user_events']: user_dict['user_events'] = '';
			return return_list


def add_user(username,user_name,*args):
	num_args = len(args)
	num_empty = 8 - num_args
	l = ['' for i in range(num_empty)]
	assert all([',' not in username,
			',' not in user_name,
			'\u2019' not in username,
			'\u2018' not in username])
	with setup_postgres.connect() as connect:
		if connect:
			conn, cur = connect
			insert_script = """INSERT INTO users (username, user_name, user_ip, user_location, user_bio,
			user_extra_bio, user_events, user_small_photo, user_large_photo, user_friends) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			l2 = [username,user_name,*args]
			l2.extend(l)
			cur.execute(insert_script,l2)
	update_users()

def add_post(username, kwargs):
	with setup_postgres.connect() as connect:
		if connect:
			conn, cur = connect
			params = post_text, post_event, post_time, post_user, post_media, post_tags = (kwargs['text'], 0,
				kwargs['date'][:10]+' '+kwargs['time'],
				username, kwargs['photo'],  '')
			insert_script = """INSERT INTO posts (post_text, post_event, post_time,
					post_user, post_media, post_tags) VALUES (%s, %s, %s, %s, %s, %s)"""
			cur.execute(insert_script, params)

def add_event(username, kwargs):
	with setup_postgres.connect() as connect:
		if connect:
			conn, cur = connect
			params = event_name, event_descr, event_location, user_posted, from_time_and_date, to_time_and_date, event_media = (kwargs['event_name'], kwargs['event_text'], kwargs['event_location'], username,
				kwargs['from_date']+' '+kwargs['from_time'], kwargs['to_date']+' '+kwargs['to_time'], kwargs['event_media'])
			insert_script = """INSERT INTO events (event_name, event_description, event_location,
					user_posted, event_date_and_time, event_ending_date_and_time, event_media) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
			cur.execute(insert_script, params)

def edit_profile_pic(username, kwargs):
	with setup_postgres.connect() as connect:
		if connect:
			conn, cur = connect
			code = "UPDATE users SET user_small_photo = %s, user_large_photo = %s WHERE username = %s";
			cur.execute(code, (kwargs['pic'], kwargs['pic'], username))


def update_users():
	global ALL_USERS_LIST, ALL_USERS
	ALL_USERS_LIST = get_all_users_list()
	ALL_USERS = get_all_users()

def update_location_preference(username,status):
	with setup_postgres.connect() as connect:
		if connect:
			conn, cur = connect
			code = "UPDATE users SET location_pref0priv1frien2pub = %s WHERE username = %s";
			cur.execute(code, (status, username))
def get_location_preference(username):
	with setup_postgres.connect() as connect:
		if connect:
			conn, cur = connect
			code = "SELECT location_pref0priv1frien2pub FROM users WHERE username = %s"
			cur.execute(code, (username,))
			status = cur.fetchall()[0]['location_pref0priv1frien2pub']
			return status


class chat:
	def add_user(username,user_name,*args):
		url = "https://api.chatengine.io/users/"
		l = user_name.split()
		payload = {"username":username, "first_name":l[0], "last_name":l[1], "secret":"123456-dummy"}
		headers = {
		  'PRIVATE-KEY': 'PKEY'
		}
		response = requests.post(url, headers=headers, data=payload)
		print("added user to chat", response.status_code)
		return 0

	def update_friends(username):
		url = "https://api.chatengine.io/chats/"
		resp = requests.get(url, data={}, headers={"Project-ID":"PID",
			"User-name":username, "User-Secret":"123456-dummy"})
		js = resp.json()
		print(f"got user friends for {username}", resp.status_code)
		new_friends = []
		for chat in js:
			p1, p2 = chat["people"][0], chat["people"][1]
			if p1["person"]["username"] == username:
				other_username = p2["person"]["username"]
			else:
				other_username = p1["person"]["username"]
			new_friends.append(other_username)
		update_script = "UPDATE users SET user_friends = %s WHERE username = %s"
		get_script = "SELECT user_friends from users WHERE username = %s"
		with setup_postgres.connect() as connect:
			if connect:
				conn, cur = connect
				cur.execute(get_script, (username,))
				current_friends = cur.fetchall()[0]["user_friends"]
				if set(new_friends) != set(current_friends.split()):
					new_friends.append(current_friends)
					all_friends = ' '.join(new_friends)
					cur.execute(update_script, (all_friends, username))
					print(f"Updated friends of {username}")
		return 0






#conn.commit()
	

#add_user("mike1","Mike Mike","","New Jersey")


