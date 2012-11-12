#! /usr/bin/python
# coding=gbk

import os
import sys
import getopt
import string

os.system('ctags  --languages=c  --langmap=c:+.pc --langmap=c:+.h --extra=+qf -R ..')
os.system('dir  /s /b ..\*.c ..\*.h ..\*.pc >cscope.files')
os.system('cscope -bCkR -i cscope.files')
curdir=os.getcwd()
os.chdir('..')
fartherdir=os.getcwd()

vimfile="C:\Program"+" Files" +"\Vim\\vimrc"

filehd=open(vimfile,'a')
filehd.write('\n')
filehd.write('\"add cscopes\n')

text=" if (filereadable(" + "\"" + curdir + "\cscope.out" + "\"))" + " && " + "expand(\"%:p:h\")==" + "\"" + fartherdir  + "\"" 
textnew=text.replace('\\','\\\\')

filehd.write(textnew+'\n')

text= "cs add " + curdir + "\cscope.out"
filehd.write(text+'\n')

text="endif"
filehd.write(text+'\n')

filehd.close()

