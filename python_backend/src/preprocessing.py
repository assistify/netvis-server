# coding=utf-8
from pymongo import MongoClient
import time
import json
import re
import nltk

import config
def init_nlp():
    print('skipped download')
    #nltk.download('punkt')

def filter_words(msg):
    tokens = []
    word = (" ".join(re.findall(r"[A-Za-züäöÜÄÖß]*", msg))).replace("  "," ")
    if (' ' in word):
        word = [w for w in nltk.word_tokenize(word) if len(w) > 2]
        tokens += word
    else:
        if (word != ''):
            tokens.append(word)
    return tokens

def load_all_data():
    start = time.time()
    client = MongoClient(config.MONGO_URL)
    db=client[config.MONGO_DB]
    rldata =dict([(r['_id'], {"t": r['t'], "name": r['fname']}) for r in db.rocketchat_room.find({"fname": { "$exists": True }, "t": { "$exists": True }}, {"t": 1, "fname": 1})]) 
    rdata = dict([(r['_id'], {"t": r['t'], "name": r['name']}) for r in db.rocketchat_room.find({"name": { "$exists": True }, "t": { "$exists": True }}, {"t": 1, "name": 1})])
    mdata = db.rocketchat_message.find({}, {"msg": 1, "rid": 1, "u": 1}).limit(config.DATA_COUNT)

    content = {}

    for i in mdata:
        if (not i['rid'] or i['rid'] == 'null' or i['rid'] == 'None'): continue
        if (not i['msg'] or i['msg'] == 'null' or i['msg'] == 'None'): continue
        if (not i['u'] or i['u'] == 'null' or i['u'] == 'None'): continue
        rid = i['rid'].encode('utf-8')
        if (not rid in rdata and not rid in rldata): continue
        room = {}
        if (rid in rdata): room = rdata[rid]
        else: room = rldata[rid]
        if (room['t'] in config.SKIP_TYPES): continue
        msg = i['msg']
        user = i['u']['username'].encode('utf-8')
        tokens = filter_words(msg)
        if (rid in content):
            content[rid]['topics'] += tokens
            if (not user in content[rid]['users']):
                content[rid]['users'].append(user)
        else:
            content[rid] = {}
            content[rid]['topics'] = tokens
            content[rid]['type'] = room['t']
            content[rid]['users'] = [user]
            content[rid]['name'] = room['name']


    end = time.time()
    print('======> Loading from DB done in : ' + str(end - start))
    return content

def remove_pretagged_words(content, tagged):
    start = time.time()
    to_tag = []
    tagged_d = dict(tagged)
    to_tag = [w for r in content for w in content[r]['topics'] if not w in tagged_d]
    end = time.time()
    print('======> Removed pretagged words in '+ str(end - start))
    return to_tag