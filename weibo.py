# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 23:39:19 2022

@author: 10310
"""

import requests
import json
import os
import pickle
import warnings

from config import TMP_PATH

if not os.path.exists(TMP_PATH):
    os.mkdir(TMP_PATH)

if not os.path.exists(os.path.join(TMP_PATH, 'history')):
    f = open(os.path.join(TMP_PATH, "history"), 'wb')
    pickle.dump([], f, 0)
    f.close()


def getHots():
    while True:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            res = requests.get("https://weibo.com/ajax/side/hotSearch")
        try:
            datas = json.loads(res.text)
            break
        except json.JSONDecodeError as e:
            print(e)
            return False

    hots = []
    hots.append(datas['data']['hotgov'])
    hots.extend(datas['data']['realtime'])
    return hots

Menus = ['word', 'num', 'label_name', 'trend']


def printMenu(hots, Menus, save=True, filter=None):

    if 'trend' in Menus:
        f = open(os.path.join(TMP_PATH, "history"), 'rb')
        history = pickle.load(f)
        f.close()
        for i, hot in enumerate(hots):
            word = hot['word']
            if word not in history:
                hot['trend'] = 'new'
            else:
                idx = history.index(word)
                if i == idx:
                    hot['trend'] = '-'
                elif i < idx:
                    hot['trend'] = '↑'
                else:
                    hot['trend'] = '↓'

    for hot in hots:
        for menu in Menus:
            if menu not in hot:
                hot[menu] = ''
        
    width = [max([len(str(hot[each])) for hot in hots] + [len(str(each))]) + 1 for each in Menus]

    if 'word' in Menus:
        charset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '
        word_lengths = []
        for hot in hots:
            this = hot['word']
            cnt = 0
            for each in this:
                if each in charset:
                    cnt += 1
                else:
                    cnt += 2
            word_lengths.append(cnt)
        width[Menus.index('word')] = max(word_lengths) + 1

    TopBar = 'id'
    for menu, wid in zip(Menus, width):
        TopBar += '\t' + menu.ljust(wid)

    print(TopBar)
    print('=' * len(TopBar))

    for i, each in enumerate(hots):
        if filter is not None:
            if not filter(each):
                continue

        thisLine = str(i)
        for wid, menu in zip(width, Menus):
            thisLine += '\t'
            if menu == 'word':
                thisLine += each[menu] + (wid - word_lengths[i]) * ' '
            else:
                thisLine += str(each[menu]).ljust(wid)
        
        print(thisLine)

    print('=' * len(TopBar))
    if save:
        data = [each['word'] for each in hots]
        f = open(os.path.join(TMP_PATH, 'history'), 'wb')
        pickle.dump(data, f, 0)
        f.close()


def filters(hot):
    return '春' in hot['word']

# printMenu(getHots(), Menus, filter=filters)