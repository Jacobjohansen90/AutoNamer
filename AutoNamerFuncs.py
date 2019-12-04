# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 23:52:21 2019

@author: Jacob
"""

import datetime
import requests
from bs4 import BeautifulSoup

def fix_case(name_list, dont_uppercase):
    for i in range(len(name_list[1:-1])):
        if name_list[i+1].lower() in dont_uppercase:
            name_list[i+1] = name_list[i+1].lower()
    for i in range(len(name_list)):
        if '-' in name_list[i]:
            words = name_list[i].split('-')
            words = [word.capitalize() for word in words]
            words = '-'.join(words)
            name_list[i] = words       
    return name_list

def log_movie(name, log_path):
    f = open(log_path, 'w+')
    log = name + ',' + str(datetime.date.today()) + '\n'
    f.write(log)
    f.close()
    
def scrape_web(string): 
    for type_ in ['(miniseries)','episodes', '(TV_series)']:
        tmp_string = string + type_
        url = requests.get(tmp_string).text
        s = BeautifulSoup(url, 'lxml')
        table = s.findAll('table',{'class':'wikitable plainrowheaders wikiepisodetable'})
        if len(table) != 0:
            type_, miniseries, tv_series, serie = type_names(type_)
            return table, type_, miniseries, tv_series, serie
        
def type_names(type_):
    if type_ == '(miniseries)':
        return type_, True, False, False
    elif type_ == '(TV_series)':
        return 'Miniseries', False, True, False
    elif type_ == 'episodes':
        return 'Serier', False, False, True

def get_names(name_list, season, manual_exceptions, corrections, no_good):
    string = 'https://en.wikipedia.org/wiki/'
    names = []
    for word in name_list:
        if word in manual_exceptions:
            index = manual_exceptions.index(word)
            word = corrections[index]
        string += word+'_'
    table, type_, miniseries, tv_series, series = scrape_web(string)
    if miniseries:
        table = table[0]
        l = table.findAll('tr')
        l = l[1:]
        for link in l:
            tmp = link.findAll('td')
            tmp = str(tmp[0])
            if 'class="description"' in tmp:
                continue
            else:
                if '</a>' in tmp:
                    tmp = tmp.split('">')
                    tmp = tmp[-1]
                    tmp = tmp.split('</a>')[0]
                    for char in tmp:
                        if char in no_good:
                            tmp = tmp.replace(char, '')
                    names.append(str(tmp))
                else:
                    tmp = tmp.split('>"')[-1]
                    tmp = tmp.split('"<')[0]
                    for char in tmp:
                        if char in no_good:
                            tmp = tmp.replace(char, ' ')
                        elif char == '&':
                            tmp.replace(char, 'and')
                    names.append(str(tmp))
        return names, type_
  
    elif tv_series:
        table = table[0]
        l = table.findAll('tr')
        l = l[1:]
        for link in l:
            tmp = link.findAll('td')
            tmp = str(tmp[1])
            if 'class="description"' in tmp:
                continue
        else:
            if '</a>' in tmp:
                tmp = tmp.split('">')
                tmp = tmp[-1]
                tmp = tmp.split('</a>')[0]
                for char in tmp:
                    if char in no_good:
                        tmp = tmp.replace(char, '')
                names.append(str(tmp))
            else:
                tmp = tmp.split('>"')[-1]
                tmp = tmp.split('"<')[0]
                for char in tmp:
                    if char in no_good:
                        tmp = tmp.replace(char, ' ')
                    elif char == '&':
                        tmp.replace(char, 'and')
                names.append(str(tmp))
        return names, type_
    
    elif series:
        table = table[int(season)-1]
        l = table.findAll('tr')
        l = l[1:]
        for link in l:
            multi_episode = False
            tmp = link.findAll('td')
            if len(link.findAll('hr'))!= 0:
                multi_episode = True
            if len(tmp) == 1:
                continue
            else:
                tmp = str(tmp[1])
            if '</a>' in tmp:
                tmp = tmp.split('">')
                tmp = tmp[-1]
                tmp = tmp.split('</a>')[0]
                for char in tmp:
                    if char in no_good:
                        tmp = tmp.replace(char, '')
                    elif char == '&':
                        tmp = tmp.replace(char, 'and')                
            else:
                tmp = tmp.split('>"')[-1]
                tmp = tmp.split('"<')[0]
                for char in tmp:
                    if char in no_good:
                        tmp = tmp.replace(char, '')
                    elif char == '&':
                        tmp = tmp.replace(char, 'and')               
            if multi_episode == True:
                names.append([True, str(tmp)])  
                names.append([True, str(tmp)])
            else:
                names.append(str(tmp))
        return names, type_
