import duckduckgo
import sys
# from subprocess import *
import os

def main(term):
    results = duckduckgo.query(str(term))
    if results.type is not 'answer':
        print results.type
    else:
        for i,result in enumerate(results.results):
            print i, result.url, result.text
        choice = int(raw_input('Open which URL?'))
        os.system('open %s' % results.results[choice].url)

if __name__ == '__main__':
    main(' '.join(sys.argv[1:]))
