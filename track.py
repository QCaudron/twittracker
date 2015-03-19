import numpy as np
import pandas as pd
import twitter as tw



# Remove problematic escape characters
def purge(s) :

	for i in ["\n", ",", "\"", "\'", "\t", "\\"] :
		s = s.replace(i, " ")

	return s.encode("utf-8")





# Read in consumer key and secret
with open("key.hidden", "r") as f :
	consumer_key = f.read().strip()

with open("secret.hidden", "r") as f :
	consumer_secret = f.read().strip()


# Authenticate
oauth_token, oauth_secret = tw.read_token_file("creds.hidden")
auth = tw.OAuth(oauth_token, oauth_secret, consumer_key, consumer_secret)
stream = tw.TwitterStream(auth=auth) # DO I NEED THIS ?




# Results
minutes = {}
users = {}
retweets = {}
counter = 0



# Grab tweets
iterator = stream.statuses.filter(track="Kanye")

for i in iterator :

	# Update counter
	counter += 1
	print counter

	# Save tweet time and username
	minutes[int(i["timestamp_ms"]) / 60000] = minutes.get(int(i["timestamp_ms"]) / 60000, 0) + 1
	users[i["user"]["name"]] = users.get(i["user"]["name"], 0) + 1
	#retweets[int(i["timestamp_ms"])] = minutes.get(int(i["timestamp_ms"]), 0) + 1

	# Every hundred tweets, write to disc
	if counter % 100 == 0 :
		pd.DataFrame(minutes.values(), index=minutes.keys(), columns=["Count"]).to_csv("minutes.csv")
