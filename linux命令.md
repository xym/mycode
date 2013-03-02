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
特别要注意一点：tr *只能进行字符的**替换、缩减和删除**，不能用来替换字符串*。

-  转为大小写
>cat oops.txt | tr "[a-z]" "[A-Z]" > result.txt

- 删除空行
>cat file | tr -s "\n" > new_file
 
- 删除Windows文件“造成”的'^M'字符
>cat file | tr -d "\r" > new_file

或者

>cat file | tr -s "\r" "\n" > new_file



