import csv
import json
import time
import tweepy
from pprint import pprint
import unicodedata


# You must use Python 2.7.x
# Rate limit chart for Twitter REST API - https://dev.twitter.com/rest/public/rate-limits

def loadKeys(key_file):
    # TODO: put your keys and tokens in the keys.json file,
    #       then implement this method for loading access keys and token from keys.json
    # rtype: str <api_key>, str <api_secret>, str <token>, str <token_secret>
    # Load keys here and replace the empty strings in the return statement with those keys
    with open(key_file, 'r') as data_file:
        data = json.load(data_file)
        api_key = data["api_key"] 
        api_secret = data["api_secret"] 
        token = data["token"] 
        token_secret = data["token_secret"]
    return api_key, api_secret, token, token_secret

# Q1.b.(i) - 5 points
def getPrimaryFriends(api, root_user, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' primary friends of 'root_user'
    # rtype: list containing entries in the form of a tuple (root_user, friend)
    primary_friends = []
    # Add code here to populate primary_friends
    for friend in tweepy.Cursor(api.friends, screen_name = root_user).items(no_of_friends):
            result = unicodedata.normalize('NFKD', friend.screen_name).encode('ascii','ignore')
            primary_friends.append((root_user,result))
    print primary_friends
    time.sleep(60)
    return primary_friends

# Q1.b.(ii) - 7 points
def getNextLevelFriends(api, friends_list, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' friends for each entry in friends_list
    # rtype: list containing entries in the form of a tuple (friends_list[i], friend)
    next_level_friends = []
    # Add code here to populate next_level_friends
    i = 0
    while i < no_of_friends:
            for friend in tweepy.Cursor(api.friends, screen_name = friends_list[i][1]).items(no_of_friends):
                result = unicodedata.normalize('NFKD', friend.screen_name).encode('ascii','ignore')
                next_level_friends.append((friends_list[i][1],result))
            print next_level_friends
            i += 1
            time.sleep(60)
    return next_level_friends

# Q1.b.(iii) - 7 points
def getNextLevelFollowers(api, followers_list, no_of_followers):
    # TODO: implement the method for fetching 'no_of_followers' followers for each entry in followers_list
    # rtype: list containing entries in the form of a tuple (follower, followers_list[i])    
    next_level_followers = []
    # Add code here to populate next_level_followers
    i = 0
    while i < no_of_followers:
            for follower in tweepy.Cursor(api.followers, screen_name = followers_list[i][1]).items(no_of_followers):
                result = unicodedata.normalize('NFKD', follower.screen_name).encode('ascii','ignore')
                next_level_followers.append((result,followers_list[i][1]))
            print next_level_followers
            i += 1
            time.sleep(60)
    return next_level_followers

# Q1.b.(i),(ii),(iii) - 4 points
def GatherAllEdges(api, root_user, no_of_neighbours):
    # TODO:  implement this method for calling the methods getPrimaryFriends, getNextLevelFriends
    #        and getNextLevelFollowers. Use no_of_neighbours to specify the no_of_friends/no_of_followers parameter.
    #        NOT using the no_of_neighbours parameter may cause the autograder to FAIL.
    #        Accumulate the return values from all these methods.
    # rtype: list containing entries in the form of a tuple (Source, Target). Refer to the "Note(s)" in the 
    #        Question doc to know what Source node and Target node of an edge is in the case of Followers and Friends. 
    all_edges = [] 
    #Add code here to populate all_edges
    primary_friends = getPrimaryFriends(api, root_user, no_of_neighbours)
    friends_list = getNextLevelFriends(api, primary_friends, no_of_neighbours)
    followers_list = getNextLevelFollowers(api, primary_friends, no_of_neighbours)
    all_edges = primary_friends + friends_list + followers_list
    return all_edges


# Q1.b.(i),(ii),(iii) - 5 Marks
def writeToFile(data, output_file):
    # write data to output_file
    # rtype: None
    with open(output_file, 'wb') as result_file:
        wr = csv.writer(result_file)
        wr.writerow(['Source','Target'])
        for row in data:
            wr.writerow(row)
    pass




"""
NOTE ON GRADING:

We will import the above functions
and use testSubmission() as below
to automatically grade your code.

You may modify testSubmission()
for your testing purposes
but it will not be graded.

It is highly recommended that
you DO NOT put any code outside testSubmission()
as it will break the auto-grader.

Note that your code should work as expected
for any value of ROOT_USER.
"""

def testSubmission():
    KEY_FILE = 'keys.json'
    OUTPUT_FILE_GRAPH = 'graph.csv'
    NO_OF_NEIGHBOURS = 20
    ROOT_USER = 'PoloChau'

    api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)

    edges = GatherAllEdges(api, ROOT_USER, NO_OF_NEIGHBOURS)
    writeToFile(edges, OUTPUT_FILE_GRAPH)

if __name__ == '__main__':
    testSubmission()


