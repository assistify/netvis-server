import argparse

import config
import preprocessing
import loader
import postprocessing
import training
import tagging
import dataTransmitter

parser = argparse.ArgumentParser()
parser.add_argument('--db', type=str, help='Database name (String)', default='SEEC')
parser.add_argument('--mongo_url', type=str, help='Mongo url (String)', default='mongodb://localhost:27017')
parser.add_argument('--server_url', type=str, help='Database name (String)', default='http://localhost:3002')
parser.add_argument('--mv', type=str, help='Model version (String)', default='0')
parser.add_argument('--corpus', type=str, help='Corpus file (String)', default='tiger_release_aug07.corrected.16012013.conll09')
parser.add_argument('--res', type=int, help='Result file number (Int)', default=13)
parser.add_argument('--datac', type=int, help='Number of data entries (Int)', default=100)
parser.add_argument('--filterw', type=int, help='Filter result by occurance (Int)', default=10)
parser.add_argument('--mpc', type=int, help='Counter for multiprocessing (Int)', default=4)
parser.add_argument('--redo_training', type=bool, help='Force retraining nlp model (Bool)', default=False)
parser.add_argument('--redo_tagging', type=bool, help='Force retagging wordlist (Bool)', default=False)
parser.add_argument('--skip_types', action='append', help='List of room types to skip (List)', default=[])
args = args = parser.parse_args()

config.init(args)

print('==============================================================')
print('NLP_MODEL_VERSION: ' + str(config.NLP_MODEL_VERSION))
print('NLP_CORPUS: ' + str(config.NLP_CORPUS))
print('RESULT_NUMBER: ' + str(config.RESULT_NUMBER))
print('DATA_COUNT: ' + str(config.DATA_COUNT))
print('FILTERW: ' + str(config.FILTERW))
print('MONGO_DB: ' + str(config.MONGO_DB))
print('FORCE_RETAG: ' + str(config.FORCE_RETAG))
print('FORCE_RETRAIN: ' + str(config.FORCE_RETRAIN))
print('SKIP_TYPES: ' + str(config.SKIP_TYPES))
print('DATA_FILENAME: ' + str(config.DATA_FILENAME))
print('TAGGING_FILENAME: ' + str(config.TAGGING_FILENAME))
print('MODEL_FILENAME: ' + str(config.MODEL_FILENAME))
print('RESULT_FILENAME: ' + str(config.RESULT_FILENAME))
print('NETVIS SERVER_URL: ' + str(config.SERVER_URL))
print('MONGO_URL: ' + str(config.MONGO_URL))
print('==============================================================')

preprocessing.init_nlp()

content = preprocessing.load_all_data()

tagged = []
if (not config.FORCE_RETAG):
    tagged = loader.load_pretagged_words()

to_tag = []
if (not config.FORCE_RETAG):
    to_tag = preprocessing.remove_pretagged_words(content, tagged)
else:
    to_tag = [w for r in content for w in r['topics']]

if (len(to_tag)):
    tagger = loader.load_model()
    tagged += tagging.start_tagging(to_tag, tagger)
    loader.save_tagged(tagged)

content = postprocessing.filter_content(content, tagged)

loader.save_json(content)

dataTransmitter.post_all_rooms(content)