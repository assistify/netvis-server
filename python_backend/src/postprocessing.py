import time
from collections import Counter

import config

def format_content(content, wcontent):
    start = time.time()
    for r in content:
        content[r]['topics'] = [{"name": n.encode('utf-8'), "weight": w, "maxWeight": wcontent[n]} for n, w in Counter(content[r]['topics']).items()]
    end = time.time()
    print('======> Reformat content done in: ' + str(end - start))
    return content

def filter_nouns(content, tagged):
    start = time.time()    
    tagged_d = dict(tagged)
    counter = 0
    for r in content:
        content[r]['topics'] = [w for w in content[r]['topics'] if w in tagged_d and tagged_d[w][0] == 'N']
        counter += len(content[r]['topics'])
    end = time.time()
    print('======> Filtering words ('+ str(counter) +') by nouns done in: ' + str(end - start))
    return content

def filter_occurance(content):
    start = time.time()
    mcontent = [w.encode('utf-8') for r in content for w in content[r]['topics']]
    wcontent = Counter(mcontent)
    counter = 0
    for r in content:
        content[r]['topics'] = [w for w in content[r]['topics'] if wcontent[w] >= config.FILTERW]
        counter += len(content[r]['topics'])
    end = time.time()
    print('======> Filtering words ('+ str(counter) +') by occurance done in: ' + str(end - start))
    return content, wcontent

def filter_content(content, tagged):
    print('======> Filtering words ('+ str(sum([len(content[t]['topics']) for t in content ])) +')')
    content = filter_nouns(content, tagged)
    content, wcontent = filter_occurance(content)
    content = format_content(content, wcontent)
    return content
