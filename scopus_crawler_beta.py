# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 14:14:27 2019

@author: Mengyu Liu
"""
from pyscopus import Scopus
import pandas
import pickle
from json import JSONDecodeError

#keys = ['d07c3456c71ef4fe35c34d8fe27b4318','30da432d73ea6cbd1ca3ce5540ea28a4',
#'6a09f4f9f223b25918ce5f0d668e33ca','e22fa0176eca805467bbf221346fad10', #'03ce6b33a244726d9d6f1ad3019f762f','eff565636066139dfb2954173c6d1d71','a9c1644234d5c8fe9665b532f494a6ec',
#'53f2ce45049139b69d36805c0fe0f471',
#'63faec376ab55a4efe9ae13be074ecc9',
#'a6f8a580279b5c667128ee42b98f446a',
#'7d5b490db9f64eea7ed5f5e741311326',
#'59086813993fc4de945e8239d5da042d']
keys = ['27839c5a7763855c5d80d3c4b197c46c','0938b72b096ed9ee75db8fa28de4724c','96a0dc33aaa7182ceee3b06e6475221c','96d06c0d77e073a795317838b9c718ca','3313f1daa25a36016da20007e82ae16f','e8a30509437a6c79d9fccf2dd94c0042','46f32bf1e1c55088a030642a17ee0a32',
'96a0dc33aaa7182ceee3b06e6475221c', '0938b72b096ed9ee75db8fa28de4724c']
scopus = Scopus(keys[0])
turn = 0
handler = open("second_year.txt", "r")
#write_handle = open("abs.txt","w")
scs = handler.readlines()
#print(len(scs))
test = scs[0]
start = '2006'
end = '2012'
epoch = 1
pandasall = []
retryflag = 0
i=0
while i < len(scs):
    print(i)
    scopusid= scs[i]
    try:
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
        kang_range['reviewer'] = scopusid
        pandasall.append(kang_range)
#        write_handle.write("\n")
#        write_handle.write("++++++++++\n")
        print(epoch)
        i+=1
    except JSONDecodeError as e:
        try:
            print("hello"+repr(e))
            scopus = Scopus(keys[turn+1])
            turn+=1
            continue
        except:
            print("Weekly quota used out! See you next week!")
            break
    except KeyError as e:
        if(retryflag):
            retryflag = 0
            i+=1
        else:
            retryflag+=1
        print(repr(e))
        continue
    except ValueError as e:
        print (e)
        i+=1
        continue
    except Exception as e:
        print("Unexpected error happened!")
        print (e)
        i+=1
        continue
result = pandas.concat(pandasall)
result.to_pickle("second_result.pkl")
result.to_csv('second_result.csv', encoding='utf-8', index=False)

#test_body = scopus.search_author_publication(test)
#print(test_body)
##test_f = test_body.dropna(axis="cover_date")
#print(test_body[(test_body['cover_date'] < '2012') & (test_body['cover_date']>'2011')])    
