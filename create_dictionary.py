import codecs
import csv
import urllib

import requests
from bs4 import BeautifulSoup
import re


def create_dictionary(web_dictionary_url, target_word, output_dir):
    print("=========================START=============================")
    print(target_word)
    print("--------------------Meanings--------------------------")
    word = urllib.parse.quote(target_word)
    code = requests.get(web_dictionary_url+word)
    plain = code.text
    s = BeautifulSoup(plain, "html.parser")
    div_word = s.find('div', {'class': 'contents'}).find('ul')
    word_list = []
    word_list_final = []
    for item in div_word:
        if 'NavigableString' not in str(type(item)):
            word_list.extend(item.contents)
    for word in word_list:
        if str(word).startswith('<page n='):
            s = BeautifulSoup(str(word), "html.parser")
            for item in s:
                for next_page_word in item.contents:
                    word_list_final.append(str(next_page_word).strip())
        else:
            word_list_final.append(str(word).strip())
    # create a dictionary
    word_meaning = {}
    key_index = 1
    key = target_word
    for index in range(1, len(word_list_final)):
        if word_list_final[index-1].startswith('<b>'):
            if re.search("<b>[0-9]+</b>", word_list_final[index-1]):
                if len(word_list_final[index].strip()) != 0 and not word_list_final[index].strip().endswith('.'):
                    word_meaning[key + '_'+ str(key_index)] = word_list_final[index]
                    key_index = key_index + 1
            if target_word in word_list_final[index-1]:
                key = word_list_final[index - 1][3:len(word_list_final[index - 1]) - 4]
                if len(word_list_final[index].strip()) != 0 and not word_list_final[index].strip().endswith('.'):
                    word_meaning[key + '_' + str(key_index)] = word_list_final[index]
                    key_index = key_index + 1
            elif '\u007E' in word_list_final[index - 2] \
                or '\u02DC' in word_list_final[index - 2] \
                or '\u0303' in word_list_final[index - 2]\
                or '\u2053' in word_list_final[index - 2]\
                or '\u223C' in word_list_final[index - 2]\
                or '\uFF5E' in word_list_final[index - 2]:
                key = target_word + word_list_final[index - 1][3:len(word_list_final[index - 1]) - 4]
                if len(word_list_final[index].strip()) != 0 and not word_list_final[index].strip().endswith('.'):
                    word_meaning[key + '_' + str(key_index)] = word_list_final[index]
                    key_index = key_index + 1
    print("===========================END===========================")
    for items in word_meaning:
        print(items + ' :: ' + word_meaning[items])
    with codecs.open(output_dir + target_word + '_dictionary.csv', 'w', 'utf-8') as file:
        writer = csv.writer(file)
        for items in word_meaning:
            writer.writerow([items, word_meaning[items]])

output_dir = 'C:/Ratul/phd/Data/Final/'
target_word_list = ['হাত', 'মাথা', 'ঘণ্টা', 'ঘর', 'পাতা', 'জল', 'যোগ']
# For testing
# target_word_list = ['পাতা']
for word in target_word_list:
    create_dictionary('http://www.bangladict.com/', word, output_dir)
