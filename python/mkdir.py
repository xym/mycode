#! /usr/bin/python
# coding=gbk

import os
import sys
import getopt
import string
value=input("�����������: ")
subvalue=input("�޸ĺ�(Ĭ��Ϊ001): ")
version=input("������汾��(Ĭ��Ϊ20120608_next), ����汾�ö��ŷֿ�: ")
grole=input("������TA��SUB(Ĭ��ΪTA)��")
pathname='��̨�����ύ_��һ��_'
dir1='��̨����'
dir2='�޸ļ�¼'
pathname2='D:\develop\TA'
pathname3='D:\develop\��TA'

if subvalue=="":
    subvalue="001"
if version=="":
    version="20120608_next"
if grole=="":
    grole="TA"
if grole.upper()=="TA":
    os.chdir(pathname2)
if grole.upper()=="SUB":
    os.chdir(pathname3)

os.mkdir(pathname+value.upper()+'_'+subvalue)
os.chdir(pathname+value.upper()+'_'+subvalue)
os.mkdir(dir1)
os.mkdir(dir2)
os.chdir(dir1)

splitver=version.upper().split(',')
for sublist in splitver:
    os.mkdir(sublist)

