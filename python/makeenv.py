#!/usr/bin/python
# coding=utf-8
import os
import commands

def chrootbashprofile():
    txt="cp /root/.bash_profile" + "  /root/.bash_profile_bak"
    os.system(txt);
    filehd=open("/root/.bash_profile",'wb')
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
    status, output = commands.getstatusoutput(' ls /home/tuxedo/bea|grep tuxedo')
    filehd.write("export TUXDIR=/home/tuxedo/bea/" + output+"\n")
    txt='''
export PATH=$TUXDIR/bin:$PATH;
export LD_LIBRARY_PATH=$TUXDIR/lib:$JVMLIBS:$LD_LIBRARY_PATH;
    '''
    filehd.write(txt)
    filehd.write("export TUXCONFIG=\"/home/"+gusername+"/bin/tuxconfig\";");

       
    filehd.write("\n")
    filehd.close()
    os.system("source  /root/.bash_profile")
    
if __name__ == "__main__":
    gusername=raw_input("please input the username that you want to create(default ta4): ")
    if len(gusername)==0:
        gusername="ta4"
    print  ("you input username is ：%s\n" % gusername)

    #修改root用户下bash_profile文件，便于使用sqlplus
    chrootbashprofile()
    print("please exit, log again!!!\n")
    os.system("sleep 1")
    

