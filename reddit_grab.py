import praw
import requests
import sys
import os
import time
import re

#Variables
subreddit = "musicbottesting"
botname = "u/throwaway176535"

waiting_list = []
if os.path.isfile('processed_comments.txt'):
    with open('processed_comments.txt','r') as file:
        processed_comments = [line.rstrip('\n') for line in file]

def main():
    reddit = praw.Reddit(client_id='',
                    client_secret='',
                    user_agent='Alter_Ego385 r_RequestABot Request',
                    username='',
                    password='')

    for comment in reddit.subreddit(subreddit).stream.comments():
        if comment.author != "AutoModerator":
            if re.search(r'\b' + botname + r'\b', comment.body):
                if comment.link_id not in processed_comments and comment.link_id not in waiting_list:
                    if "gfycat" in comment.link_url:
                        print("Processing comment {} on post {}".format(comment.id, comment.link_id))
                        link = requests.get(comment.link_url)
                        for part in link.history: # Grabbing direct object here with link.history[0] didn't work for some reason. Quick fix was to iterate through the entire list. Slightly more inefficient, but it works 
                            if "gifdeliverynetwork" in part.headers['Location']:
                                location = part.headers['Location']
                                redgifs_link = "https://redgifs.com/watch/{}".format(location[35:])
                                comment.reply("Converted Redgifs Link: {}\n\nThis action was performed by a bot, please message the moderators of this community if there was an error".format(redgifs_link))
                                print("Replied to {} with link {}".format(comment.id, redgifs_link))
                                waiting_list.append(comment.link_id)
                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
            pass

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nStopping script - writing text file first")
        with open('processed_comments.txt', 'a') as file:
            for item in waiting_list:
                file.write('{}\n'.format(item))
        time.sleep(1)
        sys.exit(0)
