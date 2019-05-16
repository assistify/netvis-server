
def init(args):
    global NLP_MODEL_VERSION
    global NLP_CORPUS
    global RESULT_NUMBER
    global DATA_COUNT
    global MONGO_DB
    global MONGO_URL
    global FORCE_RETAG
    global FORCE_RETRAIN
    global SKIP_TYPES
    global DATA_FILENAME
    global TAGGING_FILENAME
    global MODEL_FILENAME
    global RESULT_FILENAME
    global MPC
    global SERVER_URL
    global FILTERW

    NLP_MODEL_VERSION = args.mv
    NLP_CORPUS = args.corpus
    RESULT_NUMBER = args.res
    DATA_COUNT = args.datac
    FILTERW = args.filterw
    MONGO_DB = args.db.replace('"', '')
    MONGO_URL = args.mongo_url
    FORCE_RETAG = args.redo_tagging
    FORCE_RETRAIN = args.redo_training
    SKIP_TYPES = args.skip_types
    MPC = args.mpc
    SERVER_URL = args.server_url

    DATA_FILENAME = str(MONGO_DB)+'_'+str(DATA_COUNT)+'_messages_filtered.pickle'
    TAGGING_FILENAME = 'tagged_words.pickle'
    MODEL_FILENAME = 'nltk_german_classifier_data'+NLP_MODEL_VERSION+'.pickle'
    RESULT_FILENAME = 'relevant_words_result'+str(RESULT_NUMBER)+'_'+str(DATA_COUNT)