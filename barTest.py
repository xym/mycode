##############################################################################
#   本程序用于导出mysql的表，以文本形式存储
#   表migrateTable用于控制哪些表需要导出
#   目录outfiledir需要提前设置好，权限要有777，同时要注意这个目录的存储空间
#   author: xiaym
#   date: 2020-03-27
#   log:  V1.0
#         1. 文件日志、导出文件
##############################################################################

#encoding=GBK
import logging
import pymysql

####################################################################################
#是把执行的语句输出到文件中
writefileflag = True

#导出文件的目录 该目录需要有777权限
outfiledir="/root/outfiledir"

#执行脚本的输出文件名
excSQLfile="excSQLfile.sql"

#日志配置
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='outfile.log', level=logging.DEBUG, format=LOG_FORMAT)

#####################################################################################

logging.info("===========导出数据开始=============")
#打开文件
if (writefileflag):
    f = open(excSQLfile, 'w')
#数据库连接
try:
    dbconn = pymysql.Connect(
        host="192.168.137.131",
        user="root",
        passwd="root",
        charset='GBK'
    )
    tacur = dbconn.cursor()
    #
    # 读取迁移表，默认放在主库
    dbname = "hs_tabase"
    tacur.execute("use " + dbname)
    tacur.execute("select * from migrateTable")
    exeTables=tacur.fetchall()
    for t in exeTables:
        dbname = t[0]
        tablename=t[1]
        tacur.execute("use " + dbname)
        excSQL= "select *  into outfile " + "\"" + outfiledir + "/"+ tablename + "_" + dbname+ ".txt" + "\"" + " lines terminated by " + "\"" + "\\r\\n" + "\"" + " from " + tablename + ";"
        logging.info("导出表开始：" + dbname +":" + tablename )
        if (writefileflag):
            f.write(excSQL)
        logging.info("excutesql: " + excSQL)
        tacur.execute(excSQL)
        logging.info("导出表结束: " + tablename )
except pymysql.Error as e:
    logging.error(e)
    if (writefileflag):
        f.close()
    exit(-1)

tacur.close()
dbconn.close()
if (writefileflag):
    f.close()
logging.info("===========导出数据结束=============\n")
