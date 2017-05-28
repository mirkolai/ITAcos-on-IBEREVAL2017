__author__ = 'mirko'
# -*- coding: utf-8 -*-
import pymysql
import config as cfg
import glob
#dawload test data http://stel.ub.edu/Stance-IberEval2017/data.html

db = pymysql.connect(host=cfg.mysql['host'],
                     user=cfg.mysql['user'],
                     passwd=cfg.mysql['passwd'],
                     db=cfg.mysql['db'],
                     charset='utf8mb4',
                     use_unicode=True)
cur = db.cursor()
cur.execute('SET NAMES utf8mb4')
cur.execute("SET CHARACTER SET utf8mb4")
cur.execute("SET character_set_connection=utf8mb4")
db.commit()


cur.execute("truncate table `test`")
db.commit()

filelist = sorted(glob.glob("dataset/test*.txt"))

for file in filelist:
    print(file)
    infile = open(file, 'r')
    language=file[-6:-4]
    thruth=False
    if "truth" in file:
        thruth=True
    for row in infile:
        ror=row.encode("utf-8")

        if thruth:
            id=row.split(":::")[0]
            stance=row.split(":::")[1]
            gender=row.split(":::")[2]
            cur.execute("""INSERT INTO `test`(`id`,`language`, `stance`, `gender`)
        VALUES (%s,%s,%s,%s)
        on duplicate key update stance=%s and gender=%s
        """,(id,language,stance,gender,stance,gender))
            db.commit()
        else:
            id=row.split(":::")[0]
            content=row.split(":::")[1]
            cur.execute("""INSERT INTO `test`(`id`,`language`, `content`)
        VALUES (%s,%s,%s)
        on duplicate key update content=%s
        """,(id,language,content,content))
            db.commit()





