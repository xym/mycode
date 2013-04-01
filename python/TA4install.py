#!/usr/bin/python
# coding=utf-8
import os
import getpass
import string
import commands
def PRINT(string):
    print("\t" + string +"\n")

def deletedatauser():
    filename="/root/TAinstall/sql/deletesql.txt"
    logname="/root/TAinstall/log/deletedatauser.log"
    PRINT("删除数据库" + gusername + "用户")

    deletesql= " drop user " + gusername + " cascade;\n" + \
              " drop tablespace " + gusername + " including contents and datafiles;\n"
    filehd=open(filename, 'wb')
    filehd.write(deletesql)
    filehd.close()
              
    deletesql="sqlplus  -S " + gdatauser + "/" + gsystempassword +"@"+goraclesid  + " <<! \n" + \
            " set heading off \n " + \
            " set feedback off \n " + \
            " set term off \n " + \
            " spool " + logname + " \n " + \
            " @ " + filename + "\n " + \
            " spool off \n " + \
            " exit \n " + \
            " ! \n "

    PRINT("正在删除数据库用户及数据，请稍候....")
    i=os.system(deletesql);
    if i!=0:
        PRINT("删除用户失败， 参考README中的方法")
        os._exit(0)
    PRINT("删除数据库用户完成")

def  createspace():
    if gflag=="N":
        PRINT("请输入相应的值，不用输入单位!!")
        tablespacename=raw_input("请输入要创建的表空间名(默认是"+gusername+"):" )
        tablespacesize=raw_input("请输入要创建的表空间的大小(默认512M): ")
        autoincreasesize=raw_input("请输入要创建的表空间的自动增长的大小(默认100M): ")
        maxincreasesize=raw_input("请输入要创建的表空间最大值(默认1000M 输入值大于512M): ")
   
        if  tablespacesize > maxincreasesize :
            maxincreasesize=raw_input("请重新输入要创建的表空间最大值(默认1000M 不能小于创建的表空间的大小): ")
        tablespacename=getdefault(tablespacename,gusername )
        tablespacesize=getdefault(tablespacesize,"512" )
        autoincreasesize=getdefault(autoincreasesize,"100" )
        maxincreasesize=getdefault(maxincreasesize,"800" )
    else:
         tablespacename=gusername
         tablespacesize="512"
         autoincreasesize="100"
         maxincreasesize="800"

    filename="/root/TAinstall/sql/createspace.txt"
    logname="/root/TAinstall/log/createspace.log"

    createsql= " create tablespace " + gusername + " datafile \'/home/oracle/oradata/" + goraclesid +"/" + tablespacename + ".dbf\' " + "size " + tablespacesize + "M reuse AUTOEXTEND ON NEXT " + autoincreasesize + "M MAXSIZE " + maxincreasesize + "M; \n" + \
              " create user  " + gusername + " identified by  " + gusername + "  default tablespace " + tablespacename + " temporary tablespace temp QUOTA UNLIMITED ON " + tablespacename + "; \n" + \
              " grant dba,connect,resource,create table,create view to " + tablespacename + "; \n" 
    filehd=open(filename, 'wb')
    filehd.write(createsql)
    filehd.close()

    createsql="sqlplus  -S " + gdatauser + "/" +  gsystempassword +"@"+goraclesid  + " <<! \n" + \
            " set heading off \n " + \
            " set feedback off \n " + \
            " set term off \n " + \
            " spool " + logname + " \n " + \
            " @ " + filename + "\n " + \
            " spool off \n " + \
            " exit \n " + \
            " ! \n "

    PRINT("正在创建表空间，这需要几分钟，请稍候....")
    i=os.system(createsql);
    if i!=0:
        print(" 创建表空间失败, 查看createspace.log!")
        os._exit(0)
    PRINT("创建表空间完成!")

def createuser():
    PRINT("创建linux用户开始")
    tmptxt="ls /home|grep " + gusername
    existname=os.popen(tmptxt).read()
    
    if gflag=="N":
        tflag="Y"
        if cmp(existname,gusername)==True :
            PRINT("已存在用户" + gusername )
            tmptxt=raw_input("\t要删除这个用户吗？(yes/no 默认yes,按回车): ")
            tmptxt=getdefault(tmptxt,"YES")
            if  tmptxt.upper()=="YES" :
                tmptxt=" userdel -r  " + gusername  
                PRINT("正在删除用户" + gusername)
                i=os.system(tmptxt)
                if i!=0:
                    PRINT("删除用户失败。")
                PRINT("删除完成")
            else:
                tflag="N"
                
    else:
        while 1:
            tmptxt=getdata( "\t系统将删除"+gusername+"用户下所有文件!!(yes/no回车表示yes): ")
            PRINT("")
            if tmptxt.upper()=="YES"  or len(tmptxt)==0 :
                break
            else:
                 PRINT("安装退出!!")
                 os._exit(0)

        tmptxt=" userdel -r  " + gusername  
        i=os.system(tmptxt)
        if i!=0:
            PRINT("删除用户失败。")
    if tmptxt.upper()=="YES" or gflag=="Y" or (tflag=="Y" and gflag=="N"):
        PRINT("正在创建用户" + gusername)
        tmptxt="useradd -g dba " + gusername
        i=os.system(tmptxt);
        if i!=0:
            PRINT("创建用户失败。")


    createdir("/root/TAinstall/", "tmp")

    filehd=open("/root/TAinstall/tmp/userpasswd.txt", 'wb')
    filehd.write( gusername + ":" + gusername +"\n")
    filehd.close()
    PRINT("创建用户" + gusername + "密码")
    tmptxt="chpasswd " + " < " +  "/root/TAinstall/tmp/userpasswd.txt"
    i=os.system(tmptxt);
    if i!=0:
        PRINT("创建linux用户失败")
    PRINT("创建linux用户结束")


def createdir(path,filename):
    i=os.path.exists(path+filename)
    if i==False:
        os.system(" mkdir " + path + filename)
    

def modifyprofile():
    PRINT("创建.bash_profile开始")
    filehd=open('/home/' + gusername + '/' + '.bash_profile','a')
    txt='''
    # Get the aliases and functions
       if [ -f ~/.bashrc ]; then
          . ~/.bashrc
       fi
    '''
    filehd.write(txt)

    status, output = commands.getstatusoutput('cat /home/oracle/.bash_profile |grep ORACLE_BASE')
    filehd.write("# For Oracle\n")
    filehd.write(output+"\n")
    status, output = commands.getstatusoutput('cat /home/oracle/.bash_profile |grep ORACLE_HOME')
    filehd.write(output+"\n")

    status, output = commands.getstatusoutput('cat /home/oracle/.bash_profile |grep ORACLE_SID')
    filehd.write(output+"\n")

    txt='''
    export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/lib:/usr/lib:/usr/local/lib
    export PATH=$PATH:$ORACLE_HOME/bin:.
    export LANG=C
    export NLS_LANG=american_america.ZHS16GBK
    '''
    filehd.write(txt)

    filehd.write("# For Tuxedo\n")
    filehd.write("export TUXDIR=\"/home/tuxedo/bea/" + gettuxedopath() +"\""+"\n")
    txt='''
    export PATH=$TUXDIR/bin:$PATH;
    export LD_LIBRARY_PATH=$TUXDIR/lib:$JVMLIBS:$LD_LIBRARY_PATH;
    '''
    filehd.write(txt)
    filehd.write("export TUXCONFIG=\"/home/"+gusername+"/bin/tuxconfig\";");

    filehd.write("\n")

    txt='''
    # other
    export CC=/usr/bin/gcc;
    '''
    filehd.write(txt)

    filehd.write("export APPHOME=\"/home/" + gusername + "\";");

    txt='''
    export LESS_TERMCAP_md=$'\E[01;31m'
    export LESS_TERMCAP_me=$'\E[0m'
    export LESS_TERMCAP_se=$'\E[0m'
    export LESS_TERMCAP_so=$'\E[01;44;33m'
    export LESS_TERMCAP_ue=$'\E[0m'
    export LESS_TERMCAP_us=$'\E[01;32m'
    '''       
    filehd.write(txt)
    filehd.close()
    PRINT("创建.bash_profile结束")

    PRINT("加载.bash_profile开始")
    i=os.system('source /home/' + gusername + '/' + '.bash_profile')
    if i!=0:
        PRINT("加载变量失败")
    PRINT("加载.bash_profile结束")

def importdata():
    filename="/root/TAinstall/sql/impsql.txt"
    filehd=open(filename, "wb")
    tmptxt="imp " + gusername +"/" + gpasswd +"@" + goraclesid +" file=" + "/root/TAinstall/database/ta4all.dmp" + " full=y ignore=y log=/root/TAinstall/log/implog.txt  1>/dev/null 2>/dev/null  "
    filehd.write(tmptxt)
    filehd.close()

    txt="chmod +x " + filename
    os.system(txt)
    PRINT( "正在导入数据, 这需要几分钟 ....")
    i=os.system(filename)
    if i!=0:
        PRINT ("导入数据库错误！")
        os._exit(1)
    PRINT( "导入完成!")

def get_local_ip(ifname):  
    import socket, fcntl, struct  
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))  
    ret = socket.inet_ntoa(inet[20:24])  
    return ret

def createubb():
    PRINT("创建UBB.TXT开始")
    #username=getpass.getuser()
    #以下这种方式可以得到本地IP地址
    #tmptxt="  su - root -c \" ifconfig eth0 |grep -w \"inet addr\" \" "
    #print "请输入root密码"
    #IPTMP=os.popen(tmptxt).read()
    #IP=os.popen("echo " + "\"" + IPTMP + "\"" + "|cut -d: -f2 |cut -d\" \" -f1  ").read()
    #IP=IP.replace("\n","")
    IP=get_local_ip("eth0")
    MACHINENAME=getmachinename()
    filehd=open("/home/" + gusername + "/etc/ubb.txt",'wb')
    filehd.write("*RESOURCES\n")
    filehd.write("        IPCKEY                  52769 \n");
    filehd.write("        DOMAINID   " + gusername + "\n");
    filehd.write("        MASTER                  taserver \n");
    filehd.write("        MAXACCESSERS    50 \n");
    filehd.write("        MAXSERVERS      50 \n");
    filehd.write("        MAXSERVICES     80 \n");
    filehd.write("        MODEL           SHM \n");
    filehd.write("        LDBAL           N \n");
    filehd.write("*MACHINES \n");
    filehd.write("        \"" +MACHINENAME+"\"                       LMID=taserver \n");
    filehd.write("   APPDIR=\"/home/" + gusername + "/bin\" \n");
    filehd.write("   TUXCONFIG=\"/home/" + gusername + "/bin/tuxconfig\" \n");

    filehd.write("   TUXDIR=\"/home/tuxedo/bea/" + gettuxedopath()+"\""+"\n")

    filehd.write("   ULOGPFX=\"/home/" + gusername + "/log/ULOG\" \n");
    filehd.write("   MAXWSCLIENTS=10 \n");
    filehd.write("*GROUPS \n");
    filehd.write("        GROUP1                  LMID=taserver     GRPNO=1 \n");
    filehd.write("        GROUP2                  LMID=taserver     GRPNO=2 \n");
    filehd.write("*SERVERS \n");
    filehd.write("        DEFAULT: \n");
    filehd.write("        CLOPT=\"-A -t\" \n");
    filehd.write("        schedule        SRVGRP=\"GROUP1\" SRVID=1 RESTART=Y MAXGEN=2 \n");
    filehd.write("        batchsv          SRVGRP=\"GROUP1\" SRVID=2 MIN=1 MAX=8 RQADDR=QNAME REPLYQ=Y \n");
    filehd.write("        WSL             SRVGRP=\"GROUP2\" SRVID=50 CLOPT=\"-- -n //" + IP + ":" + gport + " -m 1 -M 1 -x 10\" \n");
    filehd.write("*SERVICES \n");
    filehd.close()
    PRINT("创建UBB.TXT完成")

def createmakeenv(): 
    PRINT("创建MAKEENV开始")
    os.chdir('/home/' + gusername + "/src")
    filehd=open('makeenv','wb')
    txt='''
    INCL =  -I${ORACLE_HOME}/precomp/public -I${TUXDIR}/include -I./public/ -I./schedule/
    LIB=-L${ORACLE_HOME}/lib  -lclntsh -lc -lm

    #以下用于HPUX
    #LIB=-L${ORACLE_HOME}/lib  -lclntsh

    PUB=./public/
    TRD=./trade/
    OTH=./others/
    ACCO=./acco/
    SHD=./schedule/
    INST=./install/
    TRD0=./trade0/
    TMPDIR =../tmp/
    BINDIR = ../bin/


    CFLAGS=-c -g -D_XOPEN_SOURCE
    cc=cc
    #以下用于HPUX
    #CFLAGS=-c   + DD64  -Wl, + s -D__BIGMSGQUEUE_ENABLED
    #CFLAGS=-c  + DD64, -Wl, + s -D__BIGMSGQUEUE_ENABLED

    PROC_INCL=INCLUDE=${ORACLE_HOME}/precomp/public INCLUDE=${TUXDIR}/include INCLUDE=./public/ INCLUDE=./schedule/
    '''
    filehd.write(txt)
    filehd.write("\n")
    filehd.write("OPT=ORACA=YES LINES=YES   CHAR_MAP=STRING    MODE=ORACLE    DBMS=V8 UNSAFE_NULL=YES SQLCHECK=SEMANTICS USERID=" + gusername + "/" + gusername + "@" + goraclesid +"")
    filehd.close()
    PRINT("创建makeenv结束")

    

def changeown():
    PRINT("更改文件所属组开始")
    txt="chown " + gusername + ":dba /home/" + gusername + "  -R "
    i=os.system(txt)
    if i!=0:
        PRINT("更改文件所属组失败。")
    PRINT("更改文件所属组结束")

def other():
    txt="cp /root/.bash_profile_bak" + "  /root/.bash_profile"
    os.system(txt);
    os.system("clear")
    PRINT("自动化安装脚本结束...")

    PRINT("\t信息汇总：")
    PRINT("\t===========================================")
    PRINT("\t用户名：" + gusername + "")
    PRINT("\t密码：" + gusername + "")
    PRINT("\toracle的用户名：" + gusername + "")
    PRINT("\toracle的密码：" + gusername + "")
    PRINT("\toracle的数据库标识符：" + "" + goraclesid +"" + "")
    PRINT("\t前后台通讯端口：" + gport + "")
    PRINT("\t本机地址是：" + get_local_ip("eth0") + "")
    PRINT("\t节点名称(用于ubb中)是：" + getmachinename() + "")

    PRINT("\t===========================================")

    PRINT("")
    PRINT("您还需要完成以下步骤：")
    PRINT(" 在任意路径下，执行install.sh ...")
    PRINT("")

    os.system("su - " + gusername)



def createmakefile():
    PRINT("创建MAKEFILE开始")
    filehd=open("/home/" + gusername + "/src/makefile",'wb')
    txt='''
all:    batchsv schedule
 
include makeenv

SERV=-s HS_CHK_ACCO_REQ \\
-s HS_INCR_SHARE    -s HS_REDUCE_SHARE  -s HS_PROC_STKACCO  -s HS_PRE_CLS2OPEN   -s HS_PAYMENT      \\
-s HS_PRE_SPLIT     -s HS_BREAKEVEN_NF  -s HS_PRE_BRKEVEN   -s HS_PRE_CLASS      -s HS_MDF_SHRCLASS \\
-s HS_PREBATCH0     -s HS_CHK_NSREQ     -s HS_CHK_SUBSREQ   -s HS_PREBATCH1      -s HS_OPN_FUNDACCO \\
-s HS_REG_FUNDACCO  -s HS_DR_FUNDACCO   -s HS_ADD_TRDACCO   -s HS_CLS_TRDACCO    -s HS_MDF_CUSTINFO \\
-s HS_MDF_TRDACCO   -s HS_FRZ_FUNDACCO  -s HS_DF_FUNDACCO   -s HS_CLS_FUNDACCO   -s HS_RATION_DEAL  \\
-s HS_MDF_BONUMODE  -s HS_FREEZE_SHARE  -s HS_DEFRZ_SHARE   -s HS_UNTRD_TRANS    -s HS_SUBS_DEAL    \\
-s HS_PURCHASE      -s HS_CVT_TRUSTEE   -s HS_REDEEM        -s HS_FUND_CONVERT   -s HS_PRE_BONUS    \\
-s HS_PROC_BONUS    -s HS_COMB_BONUS    -s HS_PRE_REINVEST  -s HS_REINVEST       -s HS_FUND_SETUP   \\
-s HS_ISSUE_FAIL    -s HS_FUND_CLEAR    -s HS_POST_BATCH0   -s HS_POST_BATCH1    -s HS_ADJUST_SHARE \\
-s HS_PRE_CFMRIGHT  -s HS_PROC_JT_CARD  -s HS_PRE_PAYMENT   -s HS_POST_SPLIT     -s HS_POST_CLS2OPN \\
-s HS_INITIAL       -s HS_PRE_CLRFUND   -s HS_POST_BONUS    -s HS_POST_SUBS      -s HS_VERIFY_FUND  \\
-s HS_PRE_FREDEEM   -s HS_STEP_CONFIRM  -s HS_PRE_VRFFUND   -s HS_INIT_BATCH     -s HS_PRE_REPAY    \\
-s HS_PROCMATURITY  -s HS_SPEC_BATCH0   -s HS_SPEC_BATCH1   -s HS_POSTBAT_STAT   -s HS_UNITY_DEDUCT \\
-s HS_POST_FDCLEAR  -s HS_CVT_INNTRUST  -s HS_POST_UDEDUCT  -s HS_BKUP_RECOVER   -s HS_SLT_FNDCVT   \\
-s HS_SLT_CHARGE    -s HS_PRE_SCFFRDM   -s HS_ARCHIVE

SCHEDULE=-s SCHEDULE

OBJDIR=OBJ

$(TMPDIR)spub.o:$(PUB)spub.c
        cc  $(CFLAGS) $?        $(INCL) -o $@ -lm

$(TMPDIR)accopub.o:$(ACCO)accopub.c
        cc  $(CFLAGS) $?        $(INCL) -o $@ -lm  
$(TMPDIR)accocheck.o:$(ACCO)accocheck.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c  
$(TMPDIR)accoproc.o:$(ACCO)accoproc.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c          
$(TMPDIR)othercheck.o:$(ACCO)othercheck.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c          

$(TMPDIR)fundglobal.o:$(PUB)fundglobal.pc 
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c  -o $@       $(INCL)
        rm $*.c
$(TMPDIR)fundpub.o:$(PUB)fundpub.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c     
$(TMPDIR)initialchk.o:$(TRD)initialchk.pc  
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c
$(TMPDIR)adjustshare.o:$(TRD)adjustshare.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c         
$(TMPDIR)basefunc.o:$(TRD)basefunc.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c     
$(TMPDIR)bonus.o:$(TRD)bonus.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c
$(TMPDIR)fee.o:$(TRD)fee.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c
$(TMPDIR)fundconvert.o:$(TRD)fundconvert.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c  
$(TMPDIR)income.o:$(TRD)income.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c     
$(TMPDIR)marknodeal.o:$(TRD)marknodeal.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c
$(TMPDIR)nontransactiontransfer.o:$(TRD)nontransactiontransfer.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c         
$(TMPDIR)otherrequest.o:$(TRD)otherrequest.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c    
$(TMPDIR)profit.o:$(TRD)profit.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c
$(TMPDIR)protocoldeal.o:$(TRD)protocoldeal.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c      
$(TMPDIR)redeem.o:$(TRD)redeem.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c            
$(TMPDIR)expliquidate.o:$(TRD)expliquidate.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c            
$(TMPDIR)interface.o:$(TRD)interface.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c            
$(TMPDIR)expcustomer.o:$(TRD)expcustomer.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c            
$(TMPDIR)expagency.o:$(TRD)expagency.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c            
$(TMPDIR)reqcheck.o:$(TRD)reqcheck.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c  
$(TMPDIR)reqchkimpl.o:$(TRD)reqchkimpl.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c      
$(TMPDIR)shareclass.o:$(TRD)shareclass.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c           
$(TMPDIR)specialbusinness.o:$(TRD)specialbusinness.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c           
$(TMPDIR)statistic.o:$(TRD)statistic.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c      
$(TMPDIR)subscribe.o:$(TRD)subscribe.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c     
$(TMPDIR)talaunch.o:$(TRD)talaunch.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c            
$(TMPDIR)transfertrustee.o:$(TRD)transfertrustee.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c   
$(TMPDIR)calculateincome.o:$(TRD)calculateincome.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c   
$(TMPDIR)control.o:$(TRD)control.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c   
$(TMPDIR)backup.o:$(TRD)backup.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c   
$(TMPDIR)archive.o:$(TRD)archive.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@       $(INCL)
        rm $*.c
$(TMPDIR)svccontrol.o:$(TRD)svccontrol.c
        cc  $(CFLAGS) $?        $(INCL) -o $@ 
$(TMPDIR)svcchannel.o:$(TRD)svcchannel.c  
        cc  $(CFLAGS) $?        $(INCL) -o $@ 

$(TMPDIR)implmonitor.o:$(SHD)implmonitor.c
        cc  $(CFLAGS) $?        $(INCL) -o $@ 
$(TMPDIR)monitor.o:$(SHD)monitor.c    
        cc  $(CFLAGS) $?        $(INCL) -o $@ 
$(TMPDIR)posixthread.o:$(SHD)posixthread.c
        cc  $(CFLAGS) $?        $(INCL) -o $@
$(TMPDIR)public.o:$(SHD)public.c
        cc  $(CFLAGS) $?        $(INCL) -o $@ 
$(TMPDIR)reqbroker.o:$(SHD)reqbroker.c
        cc  $(CFLAGS) $?        $(INCL) -o $@ 
$(TMPDIR)reqsender.o:$(SHD)reqsender.c
        cc  $(CFLAGS) $?        $(INCL) -o $@ 
$(TMPDIR)tathread.o:$(SHD)tathread.c  
        cc  $(CFLAGS) $?        $(INCL) -o $@ 
$(TMPDIR)tuxsender.o:$(SHD)tuxsender.c
        cc  $(CFLAGS) $?        $(INCL) -o $@ 
$(TMPDIR)accoctas.o:$(SHD)accoctas.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c            
$(TMPDIR)bizctas.o:$(SHD)bizctas.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c            
$(TMPDIR)datamodify.o:$(SHD)datamodify.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c     
$(TMPDIR)dvdctas.o:$(SHD)dvdctas.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c    
$(TMPDIR)schedule.o:$(SHD)schedule.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c
$(TMPDIR)sqlpublic.o:$(SHD)sqlpublic.pc
        proc $? oname=$*.c $(OPT) $(PROC_INCL)
        cc  $(CFLAGS) $*.c -o $@        $(INCL)
        rm $*.c

batchsv:$(TMPDIR)spub.o          $(TMPDIR)basefunc.o    $(TMPDIR)fundglobal.o         $(TMPDIR)fundpub.o     \\
         $(TMPDIR)fee.o          $(TMPDIR)subscribe.o   $(TMPDIR)otherrequest.o       $(TMPDIR)bonus.o       \\
         $(TMPDIR)protocoldeal.o $(TMPDIR)adjustshare.o $(TMPDIR)talaunch.o           $(TMPDIR)income.o      \\
         $(TMPDIR)redeem.o       $(TMPDIR)fundconvert.o $(TMPDIR)transfertrustee.o    $(TMPDIR)profit.o      \\
         $(TMPDIR)specialbusinness.o $(TMPDIR)nontransactiontransfer.o                $(TMPDIR)statistic.o   \\
         $(TMPDIR)accopub.o      $(TMPDIR)accocheck.o   $(TMPDIR)accoproc.o           $(TMPDIR)svccontrol.o  \\
         $(TMPDIR)reqcheck.o     $(TMPDIR)reqchkimpl.o  $(TMPDIR)svcchannel.o         $(TMPDIR)initialchk.o  \\
         $(TMPDIR)marknodeal.o   $(TMPDIR)shareclass.o  $(TMPDIR)othercheck.o         $(TMPDIR)control.o     \\
         $(TMPDIR)calculateincome.o $(TMPDIR)backup.o   $(TMPDIR)archive.o            $(TMPDIR)interface.o $(TMPDIR)expagency.o $(TMPDIR)expcustomer.o $(TMPDIR)expliquidate.o
        @echo BuildServer $@ ...
        buildserver     -f $(TMPDIR)spub.o        -f $(TMPDIR)basefunc.o    -f $(TMPDIR)fundglobal.o       -f $(TMPDIR)fundpub.o       \\
         -f $(TMPDIR)fee.o              -f $(TMPDIR)subscribe.o   -f $(TMPDIR)otherrequest.o     -f $(TMPDIR)bonus.o         \\
         -f $(TMPDIR)protocoldeal.o     -f $(TMPDIR)adjustshare.o -f $(TMPDIR)talaunch.o         -f $(TMPDIR)income.o        \\
         -f $(TMPDIR)redeem.o           -f $(TMPDIR)fundconvert.o -f $(TMPDIR)transfertrustee.o  -f $(TMPDIR)profit.o        \\
         -f $(TMPDIR)specialbusinness.o -f $(TMPDIR)nontransactiontransfer.o                     -f $(TMPDIR)statistic.o     \\
         -f $(TMPDIR)accopub.o          -f $(TMPDIR)accocheck.o   -f $(TMPDIR)accoproc.o         -f $(TMPDIR)svccontrol.o    \\
         -f $(TMPDIR)reqcheck.o         -f $(TMPDIR)reqchkimpl.o  -f $(TMPDIR)svcchannel.o       -f $(TMPDIR)initialchk.o    \\
         -f $(TMPDIR)marknodeal.o       -f $(TMPDIR)shareclass.o  -f $(TMPDIR)othercheck.o       -f $(TMPDIR)control.o       \\
         -f $(TMPDIR)calculateincome.o  -f $(TMPDIR)backup.o      -f $(TMPDIR)archive.o -f ${TMPDIR}interface.o -f ${TMPDIR}expagency.o -f ${TMPDIR}expcustomer.o -f ${TMPDIR}expliquidate.o \\
         -o $(BINDIR)batchsv  -f        "$(LIB)" $(SERV)
        @echo  builderserver ok! 


schedule:$(TMPDIR)implmonitor.o     $(TMPDIR)monitor.o     $(TMPDIR)posixthread.o $(TMPDIR)public.o       \\
         $(TMPDIR)reqbroker.o       $(TMPDIR)reqsender.o   $(TMPDIR)tathread.o    $(TMPDIR)accopub.o      \\
         $(TMPDIR)tuxsender.o       $(TMPDIR)bizctas.o     $(TMPDIR)control.o     $(TMPDIR)profit.o       \\
         $(TMPDIR)datamodify.o      $(TMPDIR)calculateincome.o                                            \\
         $(TMPDIR)schedule.o        $(TMPDIR)sqlpublic.o   $(TMPDIR)spub.o        $(TMPDIR)fundglobal.o   \\
         $(TMPDIR)fundpub.o         $(TMPDIR)fee.o         $(TMPDIR)reqchkimpl.o  $(TMPDIR)marknodeal.o   \\
         $(TMPDIR)subscribe.o       $(TMPDIR)initialchk.o  $(TMPDIR)reqcheck.o    $(TMPDIR)specialbusinness.o
        @echo BuildServer $@ ...
        buildserver     -f $(TMPDIR)implmonitor.o    -f $(TMPDIR)monitor.o   -f $(TMPDIR)posixthread.o -f $(TMPDIR)public.o       \\
         -f $(TMPDIR)reqbroker.o       -f $(TMPDIR)reqsender.o     -f $(TMPDIR)tathread.o    -f $(TMPDIR)accopub.o      \\
         -f $(TMPDIR)tuxsender.o       -f $(TMPDIR)bizctas.o       -f $(TMPDIR)control.o     -f $(TMPDIR)profit.o       \\
         -f $(TMPDIR)datamodify.o      -f $(TMPDIR)calculateincome.o                                                    \\
         -f $(TMPDIR)schedule.o        -f $(TMPDIR)sqlpublic.o   -f $(TMPDIR)spub.o                                     \\
         -f $(TMPDIR)fundglobal.o      -f $(TMPDIR)fundpub.o     -f $(TMPDIR)fee.o        -f $(TMPDIR)reqchkimpl.o      \\
         -f $(TMPDIR)marknodeal.o      -f $(TMPDIR)subscribe.o   -f $(TMPDIR)initialchk.o -f $(TMPDIR)reqcheck.o        \\
         -f $(TMPDIR)specialbusinness.o     \\
         -o $(BINDIR)schedule  -f       "$(LIB)" $(SCHEDULE)
        @echo  builderserver ok! 

clean::
        rm $(TMPDIR)*.o
    
'''
    filehd.write(txt)
    filehd.close()
    PRINT("创建makefile结束")

def createdatabasecfg():
    PRINT("创建etc/database.cfg开始")
    filehd=open("/home/" + gusername + "/etc/database.cfg",'wb')
    filehd.write(gusername + "/" + gusername +"@"+goraclesid)
    filehd.close()
    PRINT("创建etc/database.cfg结束")

def createmakeenv():
    PRINT("创建makeenv开始")
    filehd=open("/home/" + gusername + "/src/makeenv",'wb')
    txt='''
        INCL =  -I${ORACLE_HOME}/precomp/public -I${TUXDIR}/include -I./public/ -I./schedule/
        LIB=-L${ORACLE_HOME}/lib  -lclntsh -lc -lm  -L../tmp/

        #以下用于HPUX
        #LIB=-L${ORACLE_HOME}/lib  -lclntsh

        PUB=./public/
        TRD=./trade/
        OTH=./others/
        ACCO=./acco/
        SHD=./schedule/
        INST=./install/
        TRD0=./trade0/
        TMPDIR =../tmp/
        BINDIR = ../bin/


        #CFLAGS=-c -D_XOPEN_SOURCE
        CFLAGS=-c  -W
        cc=cc
        #以下用于HPUX
        #CFLAGS=-c   + DD64  -Wl, + s -D__BIGMSGQUEUE_ENABLED
        #CFLAGS=-c  + DD64, -Wl, + s -D__BIGMSGQUEUE_ENABLED
        '''
    filehd.write(txt)
    txt="PROC_INCL=INCLUDE=${ORACLE_HOME}/precomp/public INCLUDE=${TUXDIR}/include INCLUDE=./public/ INCLUDE=./schedule/\n"  
    filehd.write(txt)
    txt="OPT=ORACA=YES LINES=YES   CHAR_MAP=STRING       MODE=ORACLE     DBMS=V8 UNSAFE_NULL=YES SQLCHECK=SEMANTICS USERID=" + gusername + "/" + gusername +"@"+goraclesid
    filehd.write(txt)
    filehd.close()
    PRINT("创建makeenv结束")
     
def createshell():
    PRINT("创建实用shell开始")
    filehd=open("/home/" + gusername + "/bin/tarestart.sh",'wb')
    filehd.write("yes|tmipcrm\n")
    filehd.write("tmboot -y")
    filehd.close()
    filehd=open("/home/" + gusername + "/bin/makeubb.sh", 'wb')
    filehd.write("tmloadcf -y /home/" + gusername + "/etc/ubb.txt")
    filehd.close()
    
    filehd=open("/home/" + gusername + "/bin/recompile.sh", 'wb')
    filehd.write("cd /home/" + gusername + "/src; make clean \n")
    filehd.write("yes|tmipcrm || make  && tmboot -y")
    filehd.close()
    i=os.system("chmod +x " + "/home/" + gusername + "/bin/*.sh")
    if i!=0:
        PRINT("创建实用shell失败。")

    if True==os.path.exists('/home/'+gusername+'/script'):
        os.system('rm -rf '+'/home/'+gusername+'/script' )
    filepath='/home/'+gusername +"/"
    createdir(filepath, "script")

    filepath='/home/'+gusername+'/script/'
    createdir(filepath, "log")
    createdir(filepath, "database")
    createdir(filepath, "gdb")
    createdir(filepath, "mybin")
    createdir(filepath, "updatesql")
    createdir(filepath, "make")

# mybin/updatesql.sh
    filepath='/home/'+gusername+'/script'
    filename=filepath+"/mybin"+"/updatesql.sh"
    filehd=open(filename,'wb')
    filehd.write('#!/bin/bash\n')
    filehd.write('source ~/.bash_profile #加载环境变量\n')
    filehd.write('cd /home/' + gusername +'/script/mybin\n')
    filehd.write('sqlplus'+' '+gusername+'/'+gpasswd +"@"+goraclesid +' '+'<<EOF\n')
    filehd.write('@/home/'+gusername+'/script/updatesql/update.sql\n')
    filehd.write('EOF\n')
    filehd.write('rm /home/'+gusername+'/script/updatesql/update.sql\n')
    filehd.write('rm /home/'+gusername+'/script/mybin/*.log\n')
    filehd.write('exit\n')
    filehd.close()

# mybin/reboot.sh
    filename=filepath+"/mybin"+"/reboot.sh"
    filehd=open(filename,'wb')
    filehd.write('#!/bin/bash\n')
    filehd.write('source ~/.bash_profile #远程调用时，重新加载环境变量\n')
    filehd.write('#tmipcrm命令释放所有ipc资源\n')
    filehd.write('yes|tmipcrm\n')
    filehd.write('#PID=`ps -ef|grep batchsv|grep -v grep|awk \'{print $2}\'`\n')
    filehd.write('#kill ${PID}\n')
    filehd.write('tmshutdown -y\n')
    filehd.write('tmboot -y\n')
    filehd.close()

#database/dropobject.sh
    filename=filepath+"/database" +"/dropobject.sh"
    filehd=open(filename,'wb')
    filehd.write('#!/bin/bash\n')
    filehd.write('sqlplus -S ' + ' ' + gusername +'/' +gpasswd +"@"+goraclesid +'<<!\n')
    filehd.write('set heading off; \n')
    filehd.write('set feedback off; \n')
    filehd.write('spool /home/'+gusername+'/script/database/dropobj.sql; \n')
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
    filehd.write('@/home/'+gusername+'/script/database/dropobj.sql;\n')
    filehd.write('!\n')
    filehd.write('rm /home/'+gusername+'/script/database/dropobj.sql\n')
    filehd.write('exit\n')
    filehd.close

    filename=filepath+"/database" +"/truncate.sh"
    filehd=open(filename,'wb')
    filehd.write('#!/bin/bash\n')
    filehd.write('sqlplus -S ' + ' ' + gusername +'/' +gpasswd +"@"+goraclesid +'<<!\n')
    filehd.write('set heading off; \n')
    filehd.write('set feedback off; \n')
    filehd.write('spool /home/'+gusername+'/script/database/truncate.sql; \n')
    filehd.write('prompt --truncate tables \n')
    filehd.write('select \'truncate table \'||table_name ||\';\' from user_tables;  \n')
    filehd.write('\n')
    filehd.write('spool off; \n')
    filehd.write('set heading on; \n')
    filehd.write('set feedback on;  \n')
    filehd.write('\n')
    filehd.write('@/home/'+gusername+'/script/database/truncate.sql;\n')
    filehd.write('!\n')
    filehd.write('rm /home/'+gusername+'/script/database/truncate.sql\n')
    filehd.write('exit\n')
    filehd.close

    filename=filepath+"/gdb" +"/gdb.sh"
    filehd=open(filename,'wb')
    filehd.write('#!/bin/bash\n')
    filehd.write('source ~/.bash_profile\n')
    filehd.write('HOME=/home/'+gusername+'/script/gdb\n')
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
    filehd.write('PID=`ps -ef|grep batchsv|grep -v grep|grep  -w '+' ' + gusername +' '+'|awk \'{print $2}\'`\n')
    filehd.write('cd ${HOME}; gdb --pid=${PID} -x ${HOME}/gdb.txt\n')
    filehd.close()

    filename=filepath+"/gdb" +"/gdb.txt"
    filehd=open(filename,'wb')
    filehd.write('set print element 0\n')
    filehd.write('set print pretty on\n')
    filehd.write('break trd2trd.pc:Redeem\n')
    filehd.close()

    filename=filepath+"/make" +"/make.sh"
    filehd=open(filename,'wb')
    filehd.write('#!/bin/bash\n')
    filehd.write('. ~/.bash_profile #远程调用时，重新加载环境变量\n')
    filehd.write('cd /home/'+gusername+'/src\n')
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

    filename=filepath+"/mybin" +"/rmalldotfile.sh"
    filehd=open(filename,'wb')
    filehd.write('#!/bin/bash\n')
    filehd.write('rm ~/tmp/*.o \n')
    filehd.close()

    filename=filepath+"/mybin" +"/rlog.sh"
    filehd=open(filename,'wb')
    filehd.write('#!/bin/bash\n')
    filehd.write('cd ~/log;\n')
    filehd.write('rm *.log\n')
    filehd.close()
    os.system('chmod +x ' + filepath  + " -R")

    PRINT("创建实用shell结束")



def changespace2tab():
    PRINT("把空格转成TAB开始")
    filehd=open("/home/" + gusername + "/src/tab.txt",'wb')
    filehd.write(":%s/ \{3,}/\t/\n")
    filehd.write(":wq\n")
    filehd.close()
    txt="vim -s /home/" + gusername + "/src/tab.txt /home/" + gusername + "/src/makefile" + " 1>/dev/null  2>/dev/null "
    i=os.system(txt)
    if i!=0:
        PRINT("把空格转成TAB失败")
    os.system("rm  /home/" + gusername + "/src/tab.txt")
    PRINT("把空格转成TAB结束")

def cpsrc():
    tmptxt="cp -r /root/TAinstall/src/ "  + "/home/" + gusername 
    i=os.system(tmptxt)
    if i!=0:
        print "拷贝文件失败！"

def welcome():
    print ("\n\n")
    print ("\t\t\t欢迎使用TA4一键安装脚本\n")
    print ("\t\t============================================")
    print ("\t\t============================================\n")
    print ("\t\t\t编者：夏一民\n")
    print ("\t\t\t时间：2013-03-28\n")
    print ("\t\t\t版本：v.10\n")
    print ("\t\t\tE-Mail：xiaym07744@hundsun.com\n")
    print ("\t\t\t本版本提供自动安装和手动安装两个选项，推荐使用自动安装!\n")

def getdata(txt):
    val=raw_input(txt)
    return val

def getdefault(var, default):
    if len(var)==0 :
        return default
    print ("您输入的值是：%s\n" % var)
    return var
def createinstall():
    filename='/home/' + gusername + '/bin/' + 'install.sh'
    filehd=open(filename,'wb')
    filehd.write("#!/bin/bash\n")
    filehd.write("rm -rf  /home/"+gusername+"/bin/tuxconfig >/dev/null \n")
    filehd.write("tmloadcf -y " + "/home/"+gusername+"/etc/ubb.txt \n")
    filehd.write("echo -e \"正在编译源文件,请稍候.... \\n\" \n")
    filehd.write(" cd " +  "/home/"+gusername+"/src; ")
    filehd.write(" make  clean >/dev/null; " )
    filehd.write(" make " +  " -f /home/"+gusername+"/src/makefile 1>"+" /home/"+gusername+"/log/proc.log" +" 2> /home/"+gusername+"/log/makeerror.log"+" \n")
    filehd.write("        if [ $? -ne 0 ] \n");
    filehd.write("        then \n");
    filehd.write("echo -e  \"编译源文件有错！\\n\" \n")
    filehd.write("echo -e \"proc的编译日志可以查看log/proc.log !\\n \" \n")
    filehd.write("echo -e \"proc的编译错误日志可以查看log/makeerror.log !\\n \" \n")
    filehd.write("        exit\n");
    filehd.write("        fi\n");
    filehd.write("echo -e \"编译源文件结束！\\n\" \n")
    filehd.write("echo -e \"proc的编译日志可以查看log/proc.log !\\n \" \n")
    filehd.write("echo -e \"proc的编译错误日志可以查看log/makeerror.log !\\n \" \n")
    filehd.write("echo -e \"正在启动服务!\\n \" \n")
    filehd.write("        tmboot -y 1>/dev/null 2> /home/"+gusername+"/log/svc.log"+"\n");
    filehd.write("        if [ $? -ne 0 ]\n");
    filehd.write("        then\n");
    filehd.write("echo -e \"启动服务失败!\\n \" \n")
    filehd.write("echo -e \"启动服务的错误日志可以查看log/svc.log!\\n \" \n")
    filehd.write("        exit\n");
    filehd.write("        fi\n");
    filehd.write("echo -e \"服务已启动!\\n \" \n")
    filehd.write("echo -e \"启动服务的错误日志可以查看log/svc.log!\\n \" \n")
    filehd.close()
    txt="chmod +x " + filename
    os.system(txt)
    
def getmachinename():
    status, output = commands.getstatusoutput('uname -n')
    return output
def getoraclesid():
    status, oraclesid = commands.getstatusoutput('cat /home/oracle/.bash_profile |grep ORACLE_SID|awk   \'BEGIN { FS=\"=\"} {print $2}\' ')
    return oraclesid
def gettuxedopath():
    status, output = commands.getstatusoutput(' ls /home/tuxedo/bea|grep tuxedo')
    return output

if __name__ == "__main__":
    
    #欢迎界面
    welcome()

    gdatauser="system"
    gsystempassword=""
    gusername=""
    gport=""
    tmptxt=""
    
    goraclesid=getoraclesid() 
    print("系统自动获取到oracle的服务名为：" +goraclesid+"\n")
    print("系统自动获取到tuexdo的安装路径：/home/tuxedo/bea/" +gettuxedopath()+"\n")

    gsystempassword=getdata( "请输入oracle system的用户密码: ")
    if len(gsystempassword)==0:
        PRINT("密码为空!!")
        os._exit(0)
    PRINT("")

    while 1:
        tmptxt=getdata( "推荐自动安装方式!!(yes/no回车表示yes): ")
        PRINT("")
        if tmptxt.upper()=="YES"  or len(tmptxt)==0 :
            gflag="Y"
        else:
            if tmptxt.upper()=="NO":
                gflag="N"
            else:
               PRINT("输入错误,请重输!!!") 
        if tmptxt.upper() == "YES" or tmptxt.upper() == "NO" or len(tmptxt)==0 :
            break;
            


    if gflag=="N" :
        gusername=getdata( "请输入要创建的用户名（linux用户和oracle用户均用这一个,默认ta4）: ")
        gusername=getdefault(gusername, "ta4")

        gport=getdata( "请输入前台和后台通讯的端口（默认为8866）: ")
        gport=getdefault(gport,"8866")

    else:
         gusername="ta4"
         gport="8866"

    gpasswd=gusername

    PRINT("自动化安装脚本开始...")


    #创建TA4用户
    createuser()

    #创建目录
    PRINT("创建目录开始")
    dirpath="/home/"+gusername + "/"
    createdir(dirpath, "bin")
    createdir(dirpath, "etc")
    createdir(dirpath, "setup")
    createdir(dirpath, "log")
    createdir(dirpath, "src")
    createdir(dirpath, "ta4")
    createdir(dirpath, "tmp")

    dirpath="/root/TAinstall/"
    createdir(dirpath, "log")
    createdir(dirpath, "sql")
    PRINT("创建目录结束")

    #删除数据库的用户TA4
    deletedatauser()

    #修改TA4用户下bash_profile
    modifyprofile()

    #创建表空间
    createspace()


    #创建ubb.txt
    createubb()

    #创建Makefile的环境文件
    createmakeenv()
    createmakefile()


    #创建database.cfg
    createdatabasecfg()

    #生成shell
    createshell()

    #生成执行脚本
    createinstall()

    #cp src
    cpsrc()

    #改变用户所属组
    changeown()

    #导入数据库文件
    importdata()


    #转化makefile
    changespace2tab()

    #其他操作
    other()
