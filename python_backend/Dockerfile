FROM python:2.7

RUN pip install requests
RUN pip install nltk
RUN pip install pymongo

RUN python -c "exec(\"import nltk\nnltk.download('punkt')\")"

ADD src /home

WORKDIR /home
CMD python main.py --filterw=$FILTERW --datac=$DATA_COUNT --mongo_url=$MONGO_URL --server_url=$SERVER_URL --db=$MONGO_DB --skip_types=$SKIP_TYPES