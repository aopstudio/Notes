怎么查看cpu使用率、内存使用率
怎么查看某个进程使用的端口
怎么搜索出某个目录下所有包含某个字符串的所有文件
怎么对比两个文件的差异(忘了，记得有这个命令)
假设这里有nignx的日志，有访问的端口，访问的源ip等信息，如何查询访问的端口下面次数前5的源ip(不会，面试官说后面可以思考一下，经常有实际应用)
# 用户、用户组
* useradd 创建用户
* usermod 更改用户组
    * 添加用户到用户组：usermod 用户名 -aG 用户组
    * 从用户组中删除用户：usermod 用户名 -rG 用户组
* passwd 修改密码
* id 查看用户信息
* whoami 查看当前用户
* who 查看当前登录用户
* userdel 删除用户
* groups 查看用户组
* su 切换用户

# 文件权限
-rw-r--r-- 第一位如果为d，说明是目录。第一位是-代表为文件

Linux中权限基于UGO模型进行控制
* u:代表user(用户)
* g:代表group(组)
* o:代表other(其他)
* a:代表all(所有)

文件或目录的权限位是由9个权限位来控制的，每三位一组，分别是文件属主(Owner)、用户组(Group)、其他(Other)用户的读、写、执行

其中
- r(read)读权限， 可以读取文件内容，可以列出目录内容 用数字表示为4
- w(write)写权限， 可以修改文件内容，可以在目录中创建删除文件 用数字表示为2
- x(excute)执行权限，可以作为命令执行，可以访问目录内容 用数字表示为1
- 没有权限， 用数字表示为0

## 使用chown命令改变文件/目录的所属用户
修改格式：
```shell
chown 用户 文件名/目录名
```
例子
将test.txt的所属用户从root更改为demo用户
```
[root@ctos3 ~]# ls -l test.txt
-rw-r--r-- 1 root root 0 Mar 9 01:36 test.txt
[root@ctos3 ~]# chown demo test.txt #更改
[root@ctos3 ~]# ls -l test.txt
-rw-r--r-- 1 demo root 0 Mar 9 01:36 test.txt
```
### 参数介绍
-R 参数递归的修改目录下的所有文件的所属用户
#### 例子
将/test目录下的所有文件和用户所属用户修改成demo
```
[root@ctos3 ~]# chown -R demo /test/
[root@ctos3 ~]# ls -l /test/
drwxr-xr-x 3 demo root 16 Mar 9 01:55 aa
```
## 使用chgrp改变文件/目录的所属组
命令格式
```shell
chgrp 用户组 文件/目录名
```
例子：
```
[root@ctos3 ~]# chgrp demo /test/
[root@ctos3 ~]# ls -ld /test/
drwxr-xr-x 3 demo demo 16 Mar 9 01:55 /test/
```

注意点：一般都用chown修改用户和组 格式chown -R 用户.组 + 文件

## 使用chmod命令修改文件/目录的权限
命令格式
```shell
chmod +模式 +文件
```
模式为如下格式：
1. u、g、o、分别代表用户、组和其他
2. a可以代指ugo
3. +、-代表加入或删除对应权限，=代表设置对应权限
4. r、w、x代表三种权限
### 参数介绍
-R 参数递归的修改目录下的所有文件和子目录的权限
### 实例
将文件 file1.txt 设为所有人皆可读取 :
```sh
chmod ugo+r file1.txt
```
将文件 file1.txt 设为所有人皆可读取 :
```sh
chmod a+r file1.txt
```
将文件 file1.txt 与 file2.txt 设为该文件拥有者，与其所属同一个用户组者可写入，但其他人则不可写入 :
```sh
chmod ug+w,o-w file1.txt file2.txt
```
将目前目录下的所有文件与子目录皆设为任何人可读取 :
```sh
chmod -R a+r *
```
设置所属用户权限位的权限位读写:
```sh
chmod u=rw test.txt
```
所有权限为去掉执行权限
```sh
chmod a-x test.txt
```

## 使用chmod命令修改文件/目录的权限（2）
命令chmod也支持以数字方式修改权限，三个权限分别由三个数字表示：
* r=4
* w=2
* x=1

使用数字表示权限时，每组权限分别对应数字之和：
* rw=4+2＝6
* rwx＝4+2+1＝7
* r-x＝4+1＝5

语法:
```shell
chmod 755 文件或文件夹名字
```
例：
[root@centos7 ~]# touch test.txt
[root@centos7 ~]# chmod 755 test.txt

如何查看进程使用资源情况
某进程cpu占用过高怎么办

# 命令
## wc命令 
统计指定文件中的字节数、字数、行数，并将统计结果显示输出
## uniq
去除**相邻的**重复行
## sort
排序

## ln命令 
用来为文件创建链接，链接类型分为硬链接和符号链接两种，默认的链接类型是硬链接。如果要创建符号链接必须使用"-s"选项。
## >>和>
linux中经常会用到将内容输出到某文件当中，只需要在执行命令后面加上>或者>>号即可进入操作。其中>会覆盖原有文件，>>是追加内容

## 查找命令
### whereis
查找二进制程序、代码等相关文件路径
### whatis
查询一个命令执行什么功能
### which
查找并显示给定命令的绝对路径
### apropos
在 whatis 数据库中查找字符串

# 内存分区
## 代码段text
代码段在内存中被映射为只读。它是由编译器在编译链接时自动计算的。通常是用来存放程序执行的指令
## BSS
bss 是英文 Block by Symbol 的简称。通常用来存放程序中未初始化和初始化为 0的全局变量的一块内存区域
## 数据区data
通常用来存放程序中已初始化的（非 0）全局变量和静态局部变量。
## 栈stack
栈保存函数的局部变量（不包括 static 修饰的变量），参数以及返回值。
## 堆heap
堆保存函数内部动态分配（malloc 或 new）的内存

# Shell
