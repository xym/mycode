 #!/usr/bin/python
# coding=utf-8
import os
import getpass
username=getpass.getuser()
if True==os.path.exists('/home/'+username+'/script'):
    os.system('rm -rf '+'/home/'+username+'/script' )
os.mkdir('script')
os.chdir('script')
os.mkdir('log')
os.mkdir('database')
os.mkdir('gdb')
os.mkdir('mybin')
os.mkdir('make')
os.mkdir('updatesql')

# mybin/updatesql.sh
os.chdir('mybin')
filehd=open('updatesql.sh','wb')
filehd.write('#!/bin/bash\n')
filehd.write('source ~/.bash_profile #加载环境变量\n')
filehd.write('cd /home/' + username +'/script/mybin\n')
filehd.write('sqlplus'+' '+username+'/'+username +' '+'<<EOF\n')
filehd.write('@/home/'+username+'/script/updatesql/update.sql\n')
filehd.write('EOF\n')
filehd.write('rm /home/'+username+'/script/updatesql/update.sql\n')
filehd.write('rm /home/'+username+'/script/mybin/*.log\n')
filehd.write('exit\n')
filehd.close()
os.system('chmod +x updatesql.sh')

# mybin/reboot.sh
filehd=open('reboot.sh','wb')
filehd.write('#!/bin/bash\n')
filehd.write('source ~/.bash_profile #远程调用时，重新加载环境变量\n')
filehd.write('#tmipcrm命令释放所有ipc资源\n')
filehd.write('yes|tmipcrm\n')
filehd.write('#PID=`ps -ef|grep batchsv|grep -v grep|awk \'{print $2}\'`\n')
filehd.write('#kill ${PID}\n')
filehd.write('tmshutdown -y\n')
filehd.write('tmboot -y\n')
filehd.close()
os.system('chmod +x reboot.sh')

#database/dropobject.sh
os.chdir('../database')
filehd=open('dropobject.sh','wb')
filehd.write('#!/bin/bash\n')
filehd.write('sqlplus -S ' + ' ' + username +'/' +username +'<<!\n')
filehd.write('set heading off; \n')
filehd.write('set feedback off; \n')
filehd.write('spool /home/'+username+'/script/database/dropobj.sql; \n')
filehd.write('prompt --Drop constraint \n')
filehd.write('select \'alter table \'||table_name||\' drop constraint \'||constraint_name||\' ;\' from user_constraints where constraint_type=\'R\'; \n')
filehd.write('prompt --Drop tables \n')
filehd.write('select \'drop table \'||table_name ||\';\' from user_tables;  \n')
filehd.write('\n')
filehd.write('prompt --Drop view \n')
filehd.write('select \'drop view \' ||view_name||\';\' from user_views; \n')
filehd.write('\n')
filehd.write('prompt --Drop sequence \n')
filehd.write('select \'drop sequence \' ||sequence_name||\';\' from user_sequences;  \n')
filehd.write('\n')
filehd.write('prompt --Drop function \n')
filehd.write('select \'drop function \' ||object_name||\';\'  from user_objects  where object_type=\'FUNCTION\'; \n')
filehd.write('\n')
filehd.write('prompt --Drop procedure \n')
filehd.write('select \'drop procedure \'||object_name||\';\' from user_objects  where object_type=\'PROCEDURE\'; \n')
filehd.write('\n')
filehd.write('prompt --Drop package \n')
filehd.write('prompt --Drop package body \n')
filehd.write('select \'drop package \'|| object_name||\';\' from user_objects  where object_type=\'PACKAGE\'; \n')
filehd.write('select \'drop package body \'|| object_name||\';\' from user_objects  where object_type=\'PACKAGE BODY\'; \n')
filehd.write('\n')
filehd.write('prompt --Drop database link \n')
filehd.write('select \'drop database link \'|| object_name||\';\' from user_objects  where object_type=\'DATABASE LINK\'; \n')
filehd.write('\n')
filehd.write('\n')
filehd.write('spool off; \n')
filehd.write('set heading on; \n')
filehd.write('set feedback on;  \n')
filehd.write('\n')
filehd.write('@/home/'+username+'/script/database/dropobj.sql;\n')
filehd.write('!\n')
filehd.write('rm /home/'+username+'/script/database/dropobj.sql\n')
filehd.write('exit\n')
filehd.close
os.system('chmod +x dropobject.sh')


os.chdir('../gdb')
filehd=open('gdb.sh','wb')
filehd.write('#!/bin/bash\n')
filehd.write('source ~/.bash_profile\n')
filehd.write('HOME=/home/'+username+'/script/gdb\n')
filehd.write('#可以带参数r 表示先重启\n')
filehd.write('while getopts \"r\" optname\n')
filehd.write('do \n')
filehd.write('case \"$optname\" in\n')
filehd.write('"r")\n')
filehd.write('#tmshutdown -y\n')
filehd.write('yes|tmipcrm\n')
filehd.write('tmboot -y\n')
filehd.write(';;\n')
filehd.write('esac\n')
filehd.write('done\n')
filehd.write('\n')
filehd.write('PID=`ps -ef|grep batchsv|grep -v grep|grep  -w '+' ' + username +' '+'|awk \'{print $2}\'`\n')
filehd.write('cd ${HOME}; gdb --pid=${PID} -x ${HOME}/gdb.txt\n')
filehd.close()
os.system('chmod +x gdb.sh')

filehd=open('gdb.txt','wb')
filehd.write('set print element 0\n')
filehd.write('set print pretty on\n')
filehd.write('break trd2trd.pc:Redeem\n')
filehd.close()


os.chdir('../make')
filehd=open('make.sh','wb')
filehd.write('#!/bin/bash\n')
filehd.write('. ~/.bash_profile #远程调用时，重新加载环境变量\n')
filehd.write('cd /home/'+username+'/src\n')
filehd.write('\n')
filehd.write('#tmipcrm命令释放所有ipc资源\n')
filehd.write('yes|tmipcrm\n')
filehd.write('#tmshutdown -y\n')
filehd.write('make\n')
filehd.write('if [ $? -ne 0 ]   #判断执行结果是否成功\n')
filehd.write('then\n')
filehd.write('exit\n')
filehd.write('fi\n')
filehd.write('tmboot -y\n')
filehd.write('if [ $? -ne 0 ]\n')
filehd.write('then\n')
filehd.write('exit\n')
filehd.write('fi\n')
filehd.write('\n')
filehd.close()
os.system('chmod +x make.sh')

os.chdir('../mybin')
filehd=open('rmalldotfile.sh','wb')
filehd.write('#!/bin/bash\n')
if username!="zh":
    filehd.write('cd ~/src;\n')
    filehd.write('rm *.o \n')
if username=="zh":
    filehd.write('rm ~/tmp/*.o \n')
filehd.close()
os.system('chmod +x rmalldotfile.sh')


os.chdir('../mybin')
filehd=open('rmlog.sh','wb')
filehd.write('#!/bin/bash\n')
filehd.write('cd ~/log;\n')
filehd.write('rm *.log\n')
filehd.close()
os.system('chmod +x rmlog.sh')


filehd=open('/home/'+username+'/src/spub.c','a+')
text='''
int MyWriteLog(int LogLevel,char * format,...)
{
    FILE * fp;
    va_list args;
    char *ttime     = NULL;
    char ddate[9]="";
    char LogPath[50]="";
    
    ttime=GetTimeChar();
    strncpy(ddate,ttime,4);
    strncat(ddate,(ttime+5),2);
    strncat(ddate,(ttime+8),2);
    sprintf(LogPath,"../log/myfbatch%s.log",ddate);

    if (LogLevel<=GLogLevel)
    {
        if((fp=fopen(LogPath,"a+"))==NULL)
        {
            perror("Create or Open LogFile Error! GLogFile\\n");
            return -1;
        }
        fprintf(fp,"[%s]",GetTimeChar());
        va_start(args,format);
        vfprintf(fp,format,args);
        va_end(args);
        va_start(args,format);
        vprintf(format,args);   
        va_end(args);
        fclose(fp);
    }
    return 0;
}
'''
filehd.write(text);
filehd.close;

