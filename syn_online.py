'''
Created on 14/01/2013

@author: James White
https://github.com/kin3tik/

Takes a text input from the user and returns it with
each word replaced by a synonym.

Thesaurus service provided by words.bighugelabs.com
'''

import urllib.request
import json
import random
import re
import pickle
from os import path

exclude = []
thesaurus = dict()

# Given a word to search for and a type option (synonym, antonym etc),
# return a random result word from the api. If no possible results 
# exist, the original word will be returned.
# Input:     String - a word type option. 'syn'=synonym, 'ant'=antonym
#            String - the word to search for
# Return:    String - a random result word of type 'option'
def get_from_thesaurus(option, word):
    possible = []
    for word_type in thesaurus[word.lower()]:
        if option in thesaurus[word.lower()][word_type]:
            possible += thesaurus[word.lower()][word_type][option]
    if not possible:
        return word
    else:
        return pick(possible)

# Given a word to search for and a type option (synonym, antonym etc),
# return a random result word from the api. If no possible results 
# exist, the original word will be returned.
# Input:     String - a word type option. 'syn'=synonym, 'ant'=antonym
#            String - the word to search for
# Return:    String - a random result word of type 'option'
def get_from_api(option, word):
    url = 'http://words.bighugelabs.com/api/2/112142d12c570ef8d719f0ecfbd1e171/'+word+'/json'
    try:
        response = urllib.request.urlopen(url).read().decode('utf-8')
        jsob = json.loads(response)
        #if api returns a result, cache it in the thesaurus
        add_to_thesaurus(word, jsob)
        result = get_from_thesaurus(option, word)
        return result
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print('404: '+word+' not found.')
            exclude.append(word.lower())
        elif e.code == 500:
            print('500: API Limit exceeded.')
        elif e.code == 303:
            print('303: Alternate word found for '+word+'.')
        return word

# Given a word and its data, cache the data by adding
# it to the thesaurus (a dict())
# Input:     String - word to cache data for
#            JSON Object - the resulting data from the api call
def add_to_thesaurus(word, json_object):
    global thesaurus
    if not word.lower() in thesaurus:
        thesaurus[word.lower()] = json_object
        
# Randomly pick an item from a collection
# Input:     Collection - usually a list
# Return:    Single item from input collection
def pick(word_list):
    return random.choice(word_list)

# Takes an input (users input text) and splits it into an 
# array of 'words', punctuation and whitespace
# Input:     String - string to split
# Return:    Array - split string
def split_input(string):
    return re.findall(r"[\w']+|[\s.,!?;:-]", string)

# Takes the users input and returns it with each applicable word replaced
# with its 'option' word, usually a synonnym.
# Input:     String - a word type option. 'syn'=synonym, 'ant'=antonym
#            String - the users input sentence
# Return:    String - the users input sentence with 'option' words
def build_result(option, user_input):
    result = []
    processed_input = split_input(user_input)
    for word in processed_input:
        #check if the word should be processed by the API
        #skip punctuation and common words with no api results
        match = re.search('[\s\d.,!?;:]', word)
        if match or word.lower() in exclude:
            #don't consult api or thesaurus, just append back to result
            result.append(word)
        elif word.lower() in thesaurus:
            #pick a random result from the thesaurus
            result.append(get_from_thesaurus(option, word))
        else:
            #fall back to api for word data
            result.append(get_from_api(option, word))
    #concat the result array back into a String and return it
    return ''.join(result)

# Imports pickled exclusion list and thesaurus dict
def import_lists():
    #check for lists before importing
    if path.isfile("exclude.p"):
        global exclude
        exclude = pickle.load(open("exclude.p", "rb"))
    if path.isfile("thesaurus.p"):
        global thesaurus
        thesaurus = pickle.load(open("thesaurus.p", "rb"))

# Pickles exclusion list and thesaurus dict
def export_lists():
    #export/pickle lists
    pickle.dump(exclude, open("exclude.p", "wb"))
    pickle.dump(thesaurus, open("thesaurus.p", "wb"))
    
#####################################################################

import_lists()
running = True

while running:
    text = input(">> ")
    #check for termination
    if not text:
        running = False
        export_lists()
    else:
        print((build_result('syn', text)))

"""
if __name__ == "__main__":
    #usage: python [file name] [option] [input sentence]
    import sys
    import_lists()
    print((build_result(sys.argv[1], ' '.join(sys.argv[2:]))))
    export_lists()
"""