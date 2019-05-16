import pickle
import os
import time
import json

import config
import training


def load_model():
    tagger = ''
    if (os.path.isfile('data/'+config.MODEL_FILENAME)):
        start = time.time()
        with open('data/'+config.MODEL_FILENAME, 'rb') as f:
            tagger = pickle.load(f)
        end = time.time()
        print('======> Loaded model from file in: '+ str(end - start))
    else:
        tagger = training.train_nlp_model()
    return tagger

def load_pretagged_words():
    tagged = []
    start = time.time()
    if (os.path.isfile('data/'+config.TAGGING_FILENAME)):
        with open('data/'+config.TAGGING_FILENAME, 'rb') as f:
            tagged = pickle.load(f)
    end = time.time()
    print('======> Loaded tagged words from file in '+ str(end - start))
    return tagged

# def save_csv(content):
#     with open(config.RESULT_FILENAME+'.csv', 'wb') as myfile:
#         wr = csv.writer(myfile, delimiter=',', encoding='utf-8')
#         for i in relevant_words:
#             wr.writerow(i)

def save_json(content):
    with open('result/json/'+config.RESULT_FILENAME+'.json', 'wb') as myfile:
        json.dump(content, myfile)

def save_tagged(tagged):
    with open('data/'+config.TAGGING_FILENAME, 'wb') as f:
            pickle.dump(tagged, f, protocol=2)