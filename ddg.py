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
        browser = raw_input('[o]pen (default) or [l]inks? ').lower()
        print browser
        if browser in ['o', 'open', '']:
            choice = int(raw_input('Open which URL? '))
            os.system('open %s' % results.results[choice].url)
        elif browser in ['l', 'links']:
            choice = int(raw_input('Open which URL? '))
            os.system('links %s' % results.results[choice].url)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(' '.join(sys.argv[1:]))
