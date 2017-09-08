#for matilda, as I was constantly seeking help from other users by pasting code from 
#matilda.py, I kept pasting the token key by accident. I decided to seperate it to
#another file to reduce the chances of that from happening
class bottoken():
	def token(x):
		if x == "staging":
			return "<stagingtoken>"
		elif x == "live":
			return "<livetoken>"
class SQL():
	def sqlinfo(x):
		if x == "host":
			return "localhost"
		elif x == "usn":
			return "<username>"
		elif x == "pw":
			return "<password>"
		elif x == "db":
			return "<dbname>"
class admins():
	def adminlist(x):
		adminlist = ['adminuserid','adminuserid1'] #list of admin user ids. For actual live data, you do not need to put '' as the live data will be an int.
		if x in adminlist:
			return "admin"
		else:
			return "notadmin"
class errorchannel():
	def errorchannel(x):
		if x == "error":
			return "<error channel id>" #id of the channel that you're using to broadcast your error messages