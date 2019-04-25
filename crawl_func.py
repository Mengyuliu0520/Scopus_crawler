# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 09:52:59 2019

@author: Mengyu Liu
"""

from pyscopus import Scopus
import pandas

def search_for_range(filename, time_range, keys):
    '''
    file name is a file name to read scopusid of reviewers
    time range is a list of 2 string, the first is the start time , the second
    is the end time. For example:  ['2011','2012']
    keys are the created api keys, usually 10 keys could cover 70000~80000
    searches, it is a list of string, each string is a key
    
    '''
    scopus = Scopus(key)
    handler = open(filename, "r")
    #write_handle = open("abs.txt","w")
    scs = handler.readlines()
    #print(len(scs))
    #test = scs[0]
    start = time_range[0]
    end = time_range[1]
    epoch = 0
    pandasall = []
    for scopusid in scs:
        try:
            if(epoch>16000):
                scopus = Scopus(key2)
            elif(epoch>32000):
                scopus = Scopus(key3)
    #        write_handle.write("author: "+ scopusid)
    #        write_handle.write("\n")
            kang = scopus.search_author_publication(scopusid)
            epoch += 1
            kang_range = kang[(kang['cover_date'] < end) & (kang['cover_date']>start)]
            abstracts = []
            ids = kang_range['scopus_id'].tolist()
            for oneid in ids:
                abstract =scopus.retrieve_abstract(oneid)
                abstracts.append(abstract['abstract'])
    #            write_handle.write(abstract['abstract'])
    #            write_handle.write("\n")
    #            write_handle.write("**********\n")
                epoch += 1
            kang_range['abstract'] = pandas.Series(abstracts, kang_range.index)
            pandasall.append(kang_range)
    #        print(kang_range)
    #        write_handle.write("\n")
    #        write_handle.write("++++++++++\n")
            print(epoch)
        except:
            continue
    result = pandas.concat(pandasall)
    result.to_pickle("result.pkl")
    result.to_csv('result.csv', encoding='utf-8', index=False)