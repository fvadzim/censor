#-*- coding:utf-:8 -*-
with open('obscene_corpus.txt','r+') as f:
    words = sorted([line.lower().strip()+'\n' for line in f if line])
    print('Машаенька'.lower())
    f.seek(0)
    f.writelines(words)
    f.truncate()
    f.close()

