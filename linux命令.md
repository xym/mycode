#linux 命令

# __free__

----------


用法： 
 ` free -m `

主要是会看：



    [m_ta@suse:~] free -m

                  total       used       free     shared    buffers     cached

    Mem:          1534       1508         25          0         62       1243

    -/+ buffers/cache:        201       1332

    Swap:         1023         19       1004

这里有一篇文章专门讲述了这个问题: http://blog.csdn.net/tianlesoftware/article/details/6459044

我也画了一个图：
![](../../../image/blob/master/linux_free.jpg?raw=true)


#__tr__命令 

----------

tr用来从标准输入中通过替换或删除操作进行字符转换。 tr主要用于删除文件中控制字符或进行字符转换。
特别要注意一点：tr *只能进行字符的__替换、缩减和删除__，不能用来替换字符串*。

-  转为大小写
>cat oops.txt | tr "[a-z]" "[A-Z]" > result.txt

- 删除空行
>cat file | tr -s "\n" > new_file
 
- 删除Windows文件“造成”的'^M'字符
>cat file | tr -d "\r" > new_file

或者

>cat file | tr -s "\r" "\n" > new_file

# __fold__命令

----------

>fold -w Width 以变量 Width 的值指定最大行宽。缺省值为 80。 

这个命令的作用是可以把长行进行拆分：

    fold -w 80 test.txt > test.bak
    
    
# __last__ 命令


----------

列出目前与过去登入系统的用户相关信息。

这个命令可以查看哪些用户登录，在排查非法登录时，很有作用。掌握简单的一个用法就可以了。


 # last -n 15 -f  /var/log/btmp

#__ar命令__

----------

这个命令在**创建静态库**时很有用。

格式：ar rcs  libxxx.a xx1.o xx2.o

>参数r：在库中插入模块(替换)。当插入的模块名已经在库中存在，则替换同名的模块。>如果若干模块中有一个模块在库中不存在，ar显示一个错误消息，并不替换其他同名模>块。默认的情况下，新的成员增加在库的结尾处，可以使用其他任选项来改变增加的位置

>参数c：创建一个库。不管库是否存在，都将创建。

>参数s：创建目标文件索引，这在创建较大的库时能加快时间。（补充：如果不需要创建>索引，可改成大写S参数；如果.a文件缺少索引，可以使用ranlib命令添加）

 

***格式：ar -t libxxx.a***

显示库文件中有哪些目标文件，只显示名称。

 

**格式：ar -tv libxxx.a**

显示库文件中有哪些目标文件，显示文件名、时间、大小等详细信息。

 
**格式：nm -s libxxx.a**

显示库文件中的索引表。

 

***格式：ranlib libxxx.a***

为库文件创建索引表。



