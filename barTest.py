##############################################################################
#   ���������ڵ���mysql�ı����ı���ʽ�洢
#   ��migrateTable���ڿ�����Щ����Ҫ����
#   Ŀ¼outfiledir��Ҫ��ǰ���úã�Ȩ��Ҫ��777��ͬʱҪע�����Ŀ¼�Ĵ洢�ռ�
#   author: xiaym
#   date: 2020-03-27
#   log:  V1.0
#         1. �ļ���־�������ļ�
##############################################################################

#encoding=GBK
import logging
import pymysql

####################################################################################
#�ǰ�ִ�е����������ļ���
writefileflag = True

#�����ļ���Ŀ¼ ��Ŀ¼��Ҫ��777Ȩ��
outfiledir="/root/outfiledir"

#ִ�нű�������ļ���
excSQLfile="excSQLfile.sql"

#��־����
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='outfile.log', level=logging.DEBUG, format=LOG_FORMAT)

#####################################################################################

logging.info("===========�������ݿ�ʼ=============")
#���ļ�
if (writefileflag):
    f = open(excSQLfile, 'w')
#���ݿ�����
try:
    dbconn = pymysql.Connect(
        host="192.168.137.131",
        user="root",
        passwd="root",
        charset='GBK'
    )
    tacur = dbconn.cursor()
    #
    # ��ȡǨ�Ʊ�Ĭ�Ϸ�������
    dbname = "hs_tabase"
    tacur.execute("use " + dbname)
    tacur.execute("select * from migrateTable")
    exeTables=tacur.fetchall()
    for t in exeTables:
        dbname = t[0]
        tablename=t[1]
        tacur.execute("use " + dbname)
        excSQL= "select *  into outfile " + "\"" + outfiledir + "/"+ tablename + "_" + dbname+ ".txt" + "\"" + " lines terminated by " + "\"" + "\\r\\n" + "\"" + " from " + tablename + ";"
        logging.info("������ʼ��" + dbname +":" + tablename )
        if (writefileflag):
            f.write(excSQL)
        logging.info("excutesql: " + excSQL)
        tacur.execute(excSQL)
        logging.info("���������: " + tablename )
except pymysql.Error as e:
    logging.error(e)
    if (writefileflag):
        f.close()
    exit(-1)

tacur.close()
dbconn.close()
if (writefileflag):
    f.close()
logging.info("===========�������ݽ���=============\n")
