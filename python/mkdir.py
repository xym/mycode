#! /usr/bin/python
# coding=gbk

import os
import sys
import getopt
import string
value=input("请输入任务号: ")
subvalue=input("修改号(默认为001): ")
version=input("请输入版本号(默认为20120608_next), 多个版本用逗号分开: ")
grole=input("请输入TA或SUB(默认为TA)：")
pathname='后台程序提交_夏一民_'
dir1='后台程序'
dir2='修改记录'
pathname2='D:\develop\TA'
pathname3='D:\develop\分TA'

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

