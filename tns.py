from github import Github
from time import sleep
import pygame
pygame.init()
from sense_hat import SenseHat
from time import sleep
sense = SenseHat()

token = ''  # enter your github access token

def is_language(path):
    # a function to determine whether or not a path from a git tree is a language folder
    # must be a "tree" (a folder) rather than a file
    # must be 5 characters long with a hyphen in the middle e.g. "fr-CA"
    return item.type == 'tree' and len(path) == 5 and path[2] == '-'

def meow():
    beat1 = pygame.mixer.Sound('/home/pi/Desktop/sounds/meow.wav')
    beat1.play()
    sleep(1)
    beat1.play()
    sleep(1)
    beat1.play()
    sleep(1)

def sparkles():
    o = (0,0,0)
    r = (255,255,255)
    smiley_face = [o,o,o,o,o,o,o,o,
                   o,o,o,o,o,o,o,o,
                   o,o,r,o,o,r,o,o,
                   o,o,o,o,o,o,o,o,
                   o,r,o,o,o,o,r,o,
                   o,o,r,r,r,r,o,o,
                   o,o,o,o,o,o,o,o,
                   o,o,o,o,o,o,o,o]
    sense.set_pixels(smiley_face)
    sleep(1)
    sense.show_message("Hooray! Another translation!")
    sleep(1)
    sense.set_pixels(smiley_face)
    sleep(1)

# start with an empty dictionary of projects
# this will be filled with project names mapped to a set of languages
# e.g. 'storytime': {'fr-CA', 'fr-'}
projects = {}


github = Github(token)

# get all repos from the org "raspberrypilearning"
org = github.get_organization('raspberrypilearning')
repos = org.get_repos()

while True:
    for repo in repos:
        # if unknown project, add it to the dictionary
        if repo.name not in projects:
            print(f'new project: {repo.name}')
            projects[repo.name] = set()
        known_langs = projects[repo.name]  # look up known languages from last check
        try:
            last_commit = repo.get_commits()[0]  # get latest commit hash
            tree = repo.get_git_tree(last_commit.sha)  # get git tree of latest commit
            langs = set()  # create an empty set of languages
            # look for language folders in the git tree, and add them to the languages set
            for item in tree.tree:
                if is_language(item.path):
                    langs.add(item.path)
            new_langs = langs.difference(known_langs)  # compare previously known languages with now to see if there are any new ones
            projects[repo.name] = langs  # update known languages in the dictionary
            if new_langs:
                print("new language!")
                meow()
                sparkles()
                sense.clear()
            for lang in new_langs:
                print(f'{repo.name} - new language: {lang}')
        except:
            print(f'something went wrong with {repo.name}')
    sleep(60*30) # check every 30 mins
