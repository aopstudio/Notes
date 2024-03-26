## python标准数据类型，哪些是可变的哪些不可变
不可变数据（3 个）：Number（数字）、String（字符串）、Tuple（元组）；
可变数据（3 个）：List（列表）、Dictionary（字典）、Set（集合）。

Number 支持 int、float、bool、complex（复数）

Python3 中，bool 是 int 的子类，True 和 False 可以和数字相加， True==1、False==0 会返回 True，但可以通过 is 来判断类型。

## python如何判断类型
内置的 type() 函数可以用来查询变量所指的对象类型。

此外还可以用 isinstance 来判断。
```python
isinstance(obj,classinfo)
```
对于基本类型来说 classinfo 可以是：int，float，bool，complex，str(字符串)，list，dict(字典)，set，tuple

要注意的是，classinfo 的字符串是 str 而不是 string，字典也是简写 dict。

### isinstance() 与 type() 区别：
* type() 不会认为子类是一种父类类型，不考虑继承关系。
* isinstance() 会认为子类是一种父类类型，考虑继承关系。

# 讲讲Python的闭包，迭代器，拆包和封包
## 闭包
闭包就是能够读取其他函数内部变量的函数

闭包概念：在一个内部函数中，对外部作用域的变量进行引用，(并且一般外部函数的返回值为内部函数)，那么内部函数就被认为是闭包。

创建一个闭包必须满足以下几点:
* 必须有一个内嵌函数
* 内嵌函数必须引用外部函数中的变量
* 外部函数的返回值必须是内嵌函数
### 闭包的作用
闭包可以用在许多地方。它的最大用处有两个，一个是前面提到的可以读取函数内部的变量，另一个就是让这些变量的值始终保持在内存中，不会在外部函数调用后被自动清除。

闭包可以避免使用全局值，并提供某种形式的数据隐藏。它还可以为该问题提供面向对象的解决方案。
当在一个类中实现的方法很少（大多数情况下是一个方法）时，闭包可以提供另一种更优雅的解决方案。但是，当属性和方法的数量变大时，最好实现一个类。
### 代码示例
计算平均值并在每次加入新元素时都更新

#### 类实现：
```python 
class Averager(object):
    def __init__(self):
        self.series = []

    def __call__(self, new_value):
        self.series.append(new_value)
        total = sum(self.series)
        return total/len(self.series)
```
#### 闭包实现：
```python
def make_averager():
    series = []

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total/len(series)

    return averager
```

## 迭代器
一个对象要想使用 for 的方式迭代出容器内的所有数据，这就需要这个类实现「迭代器协议」。

也就是说，一个类如果实现了「迭代器协议」，就可以称之为「迭代器」。

在 Python 中，实现迭代器协议就是实现以下 2 个方法：
* __iter__：这个方法返回对象本身，即 self
* __next__：这个方法每次返回迭代的值，在没有可迭代元素时，抛出 StopIteration 异常

### 代码示例
```python
class A:
    """A 实现了迭代器协议 它的实例就是一个迭代器"""
    def __init__(self, n):
        self.idx = 0
        self.n = n

    def __iter__(self):
        print('__iter__')
        return self

    def __next__(self):
        if self.idx < self.n:
            val = self.idx
            self.idx += 1
            return val
        else:
            raise StopIteration()
# 迭代元素
a = A(3)
for i in a:
    print(i)
# 再次迭代 没有元素输出 因为迭代器只能迭代一次
for i in a:
    print(i)
```

其实，但凡是可以返回一个「迭代器」的对象，都可以称之为「可迭代对象」。

换句话说：只要__iter__ 方法返回一个迭代器，那么这个对象就是「可迭代对象」。迭代细节交给了另外一个类
```py
class B:
    # B不是迭代器 但B的实例是一个可迭代对象
    # 因为它只实现了 __iter__
    # __iter__返回了A的实例 迭代细节交给了A
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        return A(self.n)
# a是一个迭代器 同时也是一个可迭代对象
a = A(3)
for i in a:
    print(i)
# <__main__.A object at 0x10eb95550>
print(iter(a))

# b不是迭代器 但它是可迭代对象 因为它把迭代细节交给了A
b = B(3)
for i in b:
    print(i)
# <__main__.A object at 0x10eb95450>
print(iter(b))
```
总之，一个类的迭代细节，是可以交给另一个类的，就像这个例子的 B 这样，所以 B 的实例只能是「可迭代对象」，而不是「迭代器」。

其实，这种情况我们见的非常多，我们使用最多的 **list、tuple、set、dict** 类型，都只是「可迭代对象」，但不是「迭代器」，因为它们都是把迭代细节交给了另外一个类，这个类才是真正的迭代器。

```py
# list 是可迭代对象
>>> l = [1, 2]
# list 的迭代器是 list_iterator
>>> iter(l)
<list_iterator object at 0x1009c1c18>
# 执行的是 list_iterator 的 __next__
>>> iter(l).__next__()
>>> 1

# tuple 是可迭代对象
>>> t = ('a', 'b')
# tuple 的迭代器是 tuple_iterator
>>> iter(t)
<tuple_iterator object at 0x1009c1b00>
# 执行的是 tuple_iterator 的 __next__
>>> iter(t).__next__()
>>> a

# set 是可迭代对象
>>> s = {1, 2}
# set 的迭代器是 set_iterator
>>> iter(s)
<set_iterator object at 0x1009c70d8>
# 执行的是 set_iterator 的 __next__
>>> iter(s).__next__()
>>> 1

# dict 是可迭代对象
>>> d = {'a': 1, 'b': 2}
# dict 的迭代器是 dict_keyiterator
>>> iter(d)
# 执行的是 dict_keyiterator 的 __next__
<dict_keyiterator object at 0x1009c34f8>
>>> iter(d).next()
>>> a
```
## 生成器
「生成器」是一个特殊的「迭代器」，并且它也是一个「可迭代对象」。

有 2 种方式可以创建一个生成器：

* 生成器表达式
* 生成器函数

用生成器表达式创建一个生成器的例子如下：
```py
# 创建一个生成器 类型是 generator
>>> g = (i for i in range(5))
>>> g
<generator object <genexpr> at 0x101334f50>
# 生成器就是一个迭代器
>>> iter(g)
<generator object <genexpr> at 0x101334f50>
# 生成器也是一个可迭代对象
>>> for i in g:
...     print(i)
# 0 1 2 3 4
```

再来看用函数创建一个生成器：
```py
def gen(n):
    for i in range(n):
        yield i

# 创建一个生成器
g = gen(5)
# <generator object gen at 0x10bb46f50>
print(g)
# <type 'generator'>
print(type(g))

# 迭代这个生成器
for i in g:
    print(i)
# 0 1 2 3 4
```
在这个例子中，我们在函数中使用 yield 关键字。其实，包含 yield 关键字的函数，不再是一个普通的函数，而返回的是一个生成器。它在功能上与上面的例子一样，可以迭代生成器中的所有数据。

使用 yield 的函数与使用 return 的函数，在执行时的差别在于：
* 包含 return 的方法会以 return 关键字为最终返回，每次执行都返回相同的结果
* 包含 yield 的方法一般用于迭代，每次执行时遇到 yield 就返回 yield 后的结果，但内部会保留上次执行的状态，下次继续迭代时，会继续执行 yield 之后的代码，直到再次遇到 yield 后返回

当我们想得到一个集合时，如果使用普通方法，只能一次性创建出这个集合，然后 return 返回.但如果此时这个集合中的数据非常多，我们就需要在内存中一次性申请非常大的内存空间来存储。

如果我们使用 yield 生成器的方式迭代这个集合，就能解决内存占用大的问题。使用生成器创建这个集合，只有在迭代执行到 yield 时，才会返回一个元素，在这个过程中，不会一次性申请非常大的内存空间。当我们面对这种场景时，使用生成器就非常合适了。

## 拆包和封包
拆包：顾名思义就是拆开包裹，取出里面的物品。在python中就是拆开容器，然后取出里面的元素，可以一个个取，也可以将多个打包在一起取。

封包：就是把一个一个的元素封装在一起，组成一个集合。

例如：
```py
l = (1, 2, 3)
```
就可以看成是一个封包操作
```py
l = (1, 2, 3)
a = l[0]
b = l[1]
c = l[2]
```
就可以看成是一个拆包操作。

### *操作符


### **操作符

## 什么是深拷贝浅拷贝


python中import 和 from import的区别
11、python中调用系统函数，应该怎么调用
12、python装饰器说一下，以及好处，平时咋用的

python中的GIL
python的内存管理问题
*args，**kwargs区别

1  Python全局解释器

2.python数据类型
3.python装饰器
4.写个python装饰器：测程序运行时间

7.python new和init区别
8.Python多线程实现方式

- python
   - search和match
   - 垃圾回收
   - 拷贝
   - pass语句的作用

**列表和元组的区别**
python数据类型

python区分大小写吗
    装饰器
    闭包

2.Python中的迭代器和装饰器
3.Python的Magic Method
4.类中变量__name、_value的区别
5.Dict和List查询的效率差别及原因

Django请求的流程
Django的中间件了解吗
python类的内置方法有哪些，调用顺序如何，什么作用？
异常捕获
垃圾回收
restful api的规范
http状态码都有什么
python如何异步？有没有使用过异步？
python中的装饰器是什么
1. 自我介绍
2. is == 区别
3. Python 基本数据类型
4. List 和 元组 区别
5. Lambda 讲一下
6. post 有什么类型
7. 数字转字符串方法
8. 用过python哪些包
python多线程的缺点（完全不知道）
线程和协程的区别
文件操作（打开、修改、保存）使用什么方法
删除字典中的值用什么方法

1、Python的可变变量与不可变变量
2、Python迭代器、装饰器等

## 1.python线程和线程组

c，python，java的区别极其优缺点

如何遍历列表的方法
设置字典的key有什么要求

1.python基础一定要熟练，常见数据类型，如何转换，面试了10多家，经常问到的基本就是列表和字典这两种，高级用法列表推导式等必须掌握
2.python可变对象，不可变对象
3.python深浅拷贝（基本100%问到）
4.python内存管理（内存池，垃圾回收机制，不了解的赶紧去查，高频）
5.python面向对象的常用方法，如__new__和__init__区别，__call__方法，__str__,以及如何调用父类（super），以及面向对象的特性，什么是面向对象，你如何理解的等等，这些务必掌握。因为这都是最基础的，只要你背了，看了，你就有竞争力！

Python 的 list 去重，合并列表，深拷贝浅拷贝