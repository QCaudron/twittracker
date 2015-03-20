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
timestamp = {}
users = {}
counter = 0



# Grab tweets
iterator = stream.statuses.filter(track="#Science")

for i in iterator :

	# Check that all information is encoded in the tweet
	if np.all([field in i for field in ["timestamp_ms", "user"]]) :


		# Update counter
		counter += 1
		print counter

		# Save tweet time and username
		timestamp[int(i["timestamp_ms"]) / 60000] = timestamp.get(int(i["timestamp_ms"]) / 60000, 0) + 1
		users[i["user"]["name"]] = users.get(i["user"]["name"], 0) + 1
		

		# Every hundred tweets, write to disc and reset variables for memory
		if counter % 100 == 0 :
			with open("data.csv", "a") as f :
				pd.DataFrame(minutes.values(), index=minutes.keys(), columns=["Count"]).to_csv(f, header=False)
				timestamp = {}
				users = {}
