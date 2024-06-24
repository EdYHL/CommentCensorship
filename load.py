import os
import utils
import pymysql


def load_from_txt(dir_path):
    print(utils.change_color("正在加载数据", 'red'))
    words = []
    dirc = os.scandir(dir_path)
    for file in dirc:
        if file.name.endswith('.txt'):
            f = open(file, encoding='utf-8')
            for line in f:
                words.append(line.strip())
    return words


def load_from_db():
    connection = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='censors')
    cursor = connection.cursor()
    cursor.execute('SELECT word FROM blacklist')
    blacklist_db = list(cursor.fetchall())
    cursor.execute('SELECT word FROM whitelist')
    whitelist_db = list(cursor.fetchall())
    blacklist = []
    whitelist = []
    for pair in blacklist_db:
        blacklist.append(pair[0])
    for pair in whitelist_db:
        whitelist.append(pair[0])
    blacklist_db.clear()
    whitelist_db.clear()
    cursor.close()
    connection.close()
    return blacklist, whitelist
