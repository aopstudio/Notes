# python中的可变位置参数和可变关键字参数之间的区别
可变位置参数通常命名为*args，它会自动将对应位置所填的所有位置参数封包为一个元组，在函数中如果打印args这个变量，打印出来的就是一个元组

可变位置参数通常命名为**kwargs，它会自动将对应位置所填的所有关键词参数封包为一个字典，在函数中如果打印kwargs这个变量，打印出来的就是一个字典


# Django
## 中间件
中间件(middleware)允许您在一个浏览器的请求在到达Django视图之前处理它，以及在视图返回的响应到达浏览器之前处理这个响应。本文着重分析Django中间件的工作原理和应用场景，介绍如何自定义中间件并提供一些示例。

HTTP Web服务器工作原理一般都是接收用户发来的请求(request), 然后给出响应(response)。Django也不例外，其一般工作方式是接收request请求和其它参数，交由视图(view)处理，然后给出它的响应(response): 渲染过的html文件或json格式的数据。然而在实际工作中Django并不是接收到request对象后，马上交给视图函数或类(view)处理，也不是在view执行后立马把response返回给用户。**一个请求在达到视图View处理前需要先经过一层一层的中间件处理，经过View处理后的响应也要经过一层一层的中间件处理才能返回给用户**。

中间件(Middleware)在整个Django的request/response处理机制中的角色如下所示：

```py
HttpRequest -> Middleware -> View -> Middleware -> HttpResponse
```

中间件常用于权限校验、限制用户请求、打印日志、改变输出内容等多种应用场景

注意：装饰器也经常用于用户权限校验。但与装饰器不同，中间件对Django的输入或输出的改变是全局的。比如@login_required装饰器仅作用于单个视图函数。如果你希望实现全站只有登录用户才能访问，编写一个中间件是一个更好的解决方案。

## Django的中间件执行顺序
当你在settings.py注册中间件时一定要要考虑中间件的执行顺序，中间件在request到达view之前是从上向下执行的，在view执行完后返回response过程中是从下向上执行的，如下图所示。举个例子，如果你自定义的中间件有依赖于request.user，那么你自定义的中间件一定要放在AuthenticationMiddleware的后面。

## 自定义中间件
自定义中间件你首先要在app所属目录下新建一个文件middleware.py, 添加好编写的中间件代码，然后在项目settings.py中把它添加到MIDDLEWARE列表进行注册，添加时一定要注意顺序。

Django提供了两种编写自定义中间件的方式：函数和类，基本框架如下所示:

### 函数
```py
def simple_middleware(get_response):
    # 一次性设置和初始化
    def middleware(request):
        # 请求在到达视图前执行的代码
        response = get_response(request)
        # 响应在返回给客户端前执行的代码
        return response
    return middleware
```
当请求从浏览器发送到服务器视图时，将执行response = get_response(request)该行之前的所有代码。当响应从服务器返回到浏览器时，将执行response = get_response(request)此行之后的所有内容。

那么这条分界线respone = get_response(request)做什么的？简而言之，它将调用列表中的下一个中间件。如果这是最后一个中间件，则将调用该视图。

### 使用类
```py
class SimpleMiddleware:
    def __init__(self, get_response):
        # 一次性设置和初始化
        self.get_response = get_response
        
    def __call__(self, request):
        # 视图函数执行前的代码
        response = self.get_response(request)
        # 视图函数执行后的代码
        return response
```

# Python语法

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
#### *的封包操作
可以一个一个取元组或者列表中的元素：
```py
l = (1, 2, 3)
a, b, c = l
print(a, b, c)
```
这里说一下这种语句：
```py
a, b = 1, 2
```
这行代码的背后做了以下两件事情：
1. 将 1, 2 打包成一个元组。
2. 将这个元组解包，然后将得到的值分别赋值给 a 和 b。

也就是说，没有括号用逗号分开的值其实会打包成一个元组。

对于元组或者列表，也可以这样取其中的元素：
```py
l = [1, 2, 3]
a, *b = l
print(a, b)
```
结果如下：
```py
1 [2, 3]
```
具体来说，列表 l 中的元素被分配到变量 a 和 b 中：

* 第一个元素 1 被赋值给 a，
* 其余的元素 2 和 3 被打包成一个新的列表，然后赋值给 b。

也可以这样取：
```py
l = [1, 2, 3, 4]
a, *b, c = l
print(a, b, c)
```
```py
1 [2, 3] 4
```

在上面的两种拆包过程中，其实还隐含一个封包操作
a, *b = [1, 2, 3]这种语句，没有被分配到变量的那些元素会被打包成一个列表。

在这种语句中，可以理解为*增加了一个打包作用，可以打包剩余元素成列表。

#### *的拆包操作
在元组或者列表前直接加一个*号可以对其进行拆包操作：
```py
l = [1, 2, 3]
print(*l)
```
结果为：
```py
1 2 3
```
这种方式就常用于函数参数传递。
```py
def sum(a, b):
    print(a + b)
    
l = [1, 2]
sum(*l)
# 输出3
```
#### 函数参数中的*args
在python函数中，可以用*args来接受不定长参数。在这个过程中使用到了上面所说的 * 的封包和拆包的功能。

```py
def f_withoutstar(a, b, args):
    print(type(args), args)
    print(*args)
 
def f_withstar(a, b, *args):
    print(type(args), args)
    print(*args)

f_withoutstar(0, 0, (1, 2, 3))
print('-'*20)
f_withstar(0, 0, 1, 2, 3)
```

在这里的执行过程中，先把1, 2, 3通过* 封包成一个元组，赋值给args变量，这样args就是一个元组，既然是元组，也就可以用* 进行解包输出。

这样做主要就是为了在函数参数传递过程中少输两个括号。

### **操作符
#### **的拆包操作
**可以把字典拆成一个一个key = value这种形式的元素。

```py
def f(one, two):
    print(one, two)
    
dic = {'one':1, 'two':2}
f(**dic)
```
结果：
```py
1 2
```

** 把一个字典如{'one':1, 'two':2}拆成这样的形式：one=1, two=2。这样就可以用来进行参数传递。上面调用f(**dic)的语句就相当于调用f(one=1, two=2)。

下面说一下为什么不能直接打印**dict。即下面代码会报错：
```py
dic = {'one':1, 'two':2}
print(**dic)
```
print是一个函数，相当于是是print(one=1, two=2，显然print函数中没有one和two这两个关键字参数。

它们都会报如下错误：
```py
TypeError: 'one' is an invalid keyword argument for print()
```

而为什么*l可以直接打印，也就清楚了。
#### **的封包操作以及 **kwargs
**可以把函数参数中的一个一个的key=value打包成一个字典。貌似只见过在函数参数传递时用的。
```py
def f_withoutstar(a, b, kwargs):
    print(type(kwargs), kwargs)

def f_withstar(a, b, **kwargs):
    print(type(kwargs), kwargs)

f_withoutstar(0, 0, dict(one=1, two=2))
f_withstar(0, 0, one=1, two=2)
```
结果为：
```py
<class 'dict'> {'one': 1, 'two': 2}
<class 'dict'> {'one': 1, 'two': 2}
```
也就是说**它把one=1, two=2包装成了一个字典，然后赋值给kwargs变量，这样可以让我们少输一堆东西。
#### **封包和拆包合起来
```py
def sum(a, b)
    return a + b

def f(**kwargs):
    result = sum(**kwargs)
    print(result)

f(a=1, b=2)
```
结果为：
```py
3
```
在调用f时，**把a=1, b=2封包成一个字典，并赋值给变量kwargs。这样kwargs就是一个字典了，就能进行解包操作了。

在调用sum(**kwargs)时， **把字典解包成key=value的形式，然后传给sum。
### 总结
* 封包就是把元素组合成集合，拆包就是从集合中拆出元素。
* *和**都可以进行封包以及拆包操作，主要用于函数参数传递。
* 如果在函数调用语句中出现*或者**则使用的是它的拆包操作。
* 如果在函数调用语句中未出现*或者**而函数定义中却有，则此时会使用它的封包操作
# 什么是深拷贝浅拷贝
这两者的区别主要体现在对复杂对象（如列表、字典、自定义对象等）中嵌套的对象的复制行为上。

1.copy.copy 浅拷贝——只拷贝对象，不会拷贝对象的引用对象，不会拷贝原始对象的内部的
2.copy.deepcopy   深拷贝——拷贝对象的值类型，还拷贝了原始对象，而产生了一个新的对象，不仅仅只拷贝了原始对象的引用

## 浅拷贝（Shallow Copy）
浅拷贝创建一个新对象，其内容是原对象的引用的复制。这意味着如果原对象包含了对其他对象的引用（如列表中的列表），则浅拷贝会复制这些引用，而不是引用的实际对象。因此，如果你修改了原对象中嵌套对象的内容，这些修改也会反映在浅拷贝的对象上，反之亦然。

浅拷贝可以通过copy()方法、dict.copy()方法、或者copy模块中的copy.copy()函数实现。

浅拷贝适用于原对象不包含任何对可变对象的引用，或者你不打算修改任何内部可变对象的情况。
## 深拷贝（Deep Copy）
深拷贝创建一个新对象，然后递归地复制原对象中的所有对象。这意味着不仅原对象被复制，所有内部的容器对象以及它们包含的任何东西都会被复制。因此，原对象和深拷贝对象之间不会共享任何对象（除了那些特别指定为共享的）。

深拷贝可以通过copy模块中的copy.deepcopy()函数实现。

深拷贝适用于原对象包含对可变对象的引用，并且你需要一个完全独立的对象副本，修改副本不会影响原对象的情况。
## 总结
* 性能考虑：深拷贝会复制原对象中的所有元素，因此比浅拷贝消耗更多的内存和处理时间。
* 使用场景：选择浅拷贝还是深拷贝取决于你的具体需求。如果对象中包含了复杂的嵌套结构，并且你需要一个完全独立的副本，那么应该使用深拷贝。如果你只需要复制对象的顶层结构，不需要独立复制内部元素，或者你确信不会修改任何嵌套对象，那么浅拷贝是更合适的选择。
## 补充
Python 内不可变对象的内存管理方式是引用计数。因此，我们在谈论拷贝时，其实谈论的主要特点都是基于可变对象的。我们来看下面这段代码
```py
import copy

a = "张小鸡"
b = a
c = copy.copy(a)
d = copy.deepcopy(a)

print "赋值：id(b)->>>", id(b)
print "浅拷贝：id(c)->>>", id(c)
print "深拷贝：id(d)->>>", id(c)
```
输出如下：
```py
赋值：id(b)->>> 4394180400
浅拷贝：id(c)->>> 4394180400
深拷贝：id(d)->>> 4394180400
```
因为我们这里操作的是不可变对象，Python 用引用计数的方式管理它们，所以 Python 不会对值相同的不可变对象，申请单独的内存空间。只会记录它的引用次数。

在操作被拷贝对象内部的不可变对象时，浅拷贝和深拷贝是没有区别的

浅拷贝后在操作被拷贝对象内部的可变元素时，其结果是会影响到拷贝对象的

## 最终总结
1. 由于 Python 内部引用计数的特性，对于不可变对象，浅拷贝和深拷贝的作用是一致的，就相当于复制了一份副本，原对象内部的不可变对象的改变，不会影响到复制对象
2. 浅拷贝的拷贝。其实是拷贝了原始元素的引用（内存地址），所以当拷贝可变对象时，原对象内可变对象的对应元素的改变，会在复制对象的对应元素上，有所体现
3. 深拷贝在遇到可变对象时，又在内部做了新建了一个副本。所以，不管它内部的元素如何变化，都不会影响到原来副本的可变对象

# Python引用计数
引用计数是一种最直观，最简单的垃圾收集技术。原理非常简单，每一个对象都包含了两个头部信息，一个是类型标志符，标识这个对象的类型；另一个是计数器，记录当前指向该对象的引用数目，表示这个对象被多少个变量名所引用。

CPython 使用引用计数来管理内存，所有 Python 脚本中创建的实例，都会有一个引用计数，来记录有多少个指针指向它。当引用计数只有 0 时，则会自动释放内存。

Python垃圾回收主要以引用计数为主，分代回收为辅。引用计数法的原理是每个对象维护一个ob_ref，用来记录当前对象被引用的次数，也就是来追踪到底有多少引用指向了这个对象，当发生以下四种情况的时候，该对象的引用计数器+1

* 对象被创建  a=14
* 对象被引用  b=a
* 对象被作为参数,传到函数中   func(a)
* 对象作为一个元素，存储在容器中   List={a,”a”,”b”,2}

与上述情况相对应，当发生以下四种情况时，该对象的引用计数器-1

* 当该对象的别名被显式销毁时  del a
* 当该对象的引别名被赋予新的对象，   a=26
* 一个对象离开它的作用域，例如 func函数执行完毕时，函数里面的局部变量的引用计数器就会减一（但是全局变量不会）
* 将该元素从容器中删除时，或者容器被销毁时。

当指向该对象的内存的引用计数器为0的时候，该内存将会被Python虚拟机销毁

## 原始的引用计数法存在的问题

1. 维护引用计数消耗资源，维护引用计数的次数和引用赋值成正比，而不像mark and sweep等基本与回收的内存数量有关。
2. 无法解决循环引用的问题。A和B相互引用而再没有外部引用A与B中的任何一个（循环引用），它们的引用计数都为1，但显然应该被回收。

# python中import 和 from import的区别
使用import语句时，通常是引入整个模块，然后通过模块名加.访问模块中的属性、函数或类。
使用from ... import ...语句时，可以从模块中直接引入特定的属性、函数或类，不需要使用模块名作为前缀

# python中调用系统函数，应该怎么调用


# python装饰器说一下，以及好处，平时咋用的
接下来就讲装饰器，其实装饰器就是一个闭包，装饰器是闭包的一种应用。什么是装饰器呢，简言之，python装饰器就是用于拓展原来函数功能的一种函数，这个函数的特殊之处在于它的返回值也是一个函数

使用python装饰器的好处就是在不用更改原函数的代码前提下给函数增加新的功能。使用时，再需要的函数前加上@demo（装饰器函数名）即可。

```python
def debug(func):
    def wrapper():
        print("[DEBUG]: enter {}()".format(func.__name__))
        return func()
    return wrapper

@debug
def hello():
    print("hello")

hello()
```
例子中的装饰器给函数加上一个进入函数的debug模式，不用修改原函数代码就完成了这个功能，可以说是很方便了。

## 写个python装饰器：测程序运行时间
```py
def cal_time(func):
    def wrapper():
        before_time=time.time()
        func()
        after_time=time.time()
        print("the func run time is {}".format(after_time-before_time))
    return wrapper

@cal_time
def hello():
    print("hello")
```
# python中的GIL（全局解释器锁）
## GIL 全局解释器锁
GIL虽然从设计的出发点就是考虑到线程安全，但这种线程安全是粗粒度的线程安全，即不需要程序员自己对线程进行加锁处理（同理，所谓细粒度就是指程序员需要自行加、解锁来保证线程安全，典型代表是 Java , 而 CPthon 中是粗粒度的锁，即语言层面本身维护着一个全局的锁机制,用来保证线程安全）。

如何解决线程安全问题？CPython 解释器使用了加锁的方法。每个进程有一把锁，启动线程先加锁，结束线程释放锁。打个比方，进程是一个厂房，厂房大门是开着的，门内有锁，工人进入大门后可以在内部上锁。厂房里面有 10 个车间对应 10 个线程，每个 CPU 就是一个工人。GIL（Global Interpreter Lock）全局锁就相当于厂房规定：工人要到车间工作，从厂房大门进去后要在里面反锁，完成工作后开锁出门，下一个工人再进门上锁。也就是说，任意时刻厂房里只能有一个工人，但这样就保证了工作的安全性，这就是 GIL 的原理。当然了，GIL 的存在有很多其它益处，包括简化 CPython 解释器和大量扩展的实现。

根据上面的例子可以看出 GIL 实现了线程操作的安全性，但多线程的效率被大打折扣，一个工厂里只能有一个工人干活，很难想象。这也是 David Beazley（《Python 参考手册》和《Python Cookbook》的作者）说 “Python 线程毫无用处” 的原因。

注意，GIL 不是语言特性，而是解释器的设计特点，有些 Python 解释器例如 JPython 就没有 GIL ，除了 Python 其它语言也有 GIL 设计，例如 Ruby 。

## 如何避免GIL的影响

1. 在以IO操作为主的IO密集型应用中，多线程和多进程的性能区别并不大，原因在于即使在Python中有GIL锁的存在，由于线程中的IO操作会使得线程立即释放GIL，切换到其他非IO线程继续操作，提高程序执行效率。相比进程操作，线程操作更加轻量级，线程之间的通讯复杂度更低，建议使用多线程。

2. 如果是计算密集型的应用，尽量使用多进程或者协程来代替多线程


# *args，**kwargs区别
*args可以将对应位置的一个或多个参数封包成一个元组

**kwargs可以将对应位置的一个或多个key=value形式的参数封包成一个字典

# 设置字典的key有什么要求
必须是不可变类型，比如Number，String，Tuple，不能是可变类型Dict，List，Set
# 列表和元组的区别
列表是动态数组，它们可变且可以重设长度（改变其内部元素的个数）。
元组是静态数组，它们不可变，且其内部数据一旦创建便无法改变。

对于长度为1~20的元组，即使它们不在被使用，它们的空间也不会立刻还给系统，而是留待未来使用。这意味着当未来需要一个同样大小的新的元组时，我们不再需要向操作系统申请一块内存来存放数据，因为我们已经有了预留的空间。

# python面向对象的常用方法
## Python中的__init__和__new__
__init__函数并不是真正意义上的构造函数，__init__方法做的事情是在对象创建好之后初始化变量。真正创建实例的是__new__方法

实例化了一个Person对象，可以看到__new__和__init__都被调用了。__new__方法用于创建对象并返回对象，当返回对象时会自动调用__init__方法进行初始化。
init是在类实例创建之后调用，而 new方法正是创建这个类实例的方法。
__new__方法是类方法，而__init__是实例方法。

### 用__new__方法实现单例模式
```py
class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

s1 = Singleton()
s2 = Singleton()
print(s1)
print(s2) 
``` 

### 用__new__方法实现简单工厂模式
```py
class Fruit(object):
    def __init__(self):
        pass

    def print_color(self):
        pass

class Apple(Fruit):
    def __init__(self):
        pass

    def print_color(self):
        print("apple is in red")

class Orange(Fruit):
    def __init__(self):
        pass

    def print_color(self):
        print("orange is in orange")

class FruitFactory(object):
    fruits = {"apple": Apple, "orange": Orange}

    def __new__(cls, name):
        if name in cls.fruits.keys():
            return cls.fruits[name]()
        else:
            return Fruit()

fruit1 = FruitFactory("apple")
fruit2 = FruitFactory("orange")
fruit1.print_color()    
fruit2.print_color()    
```
## __call__方法
python的__call__()是一种magic method，在类中实现这一方法可以使该类的实例（对象）像函数一样被调用。默认情况下该方法在类中是没有被实现的。使用callable()方法可以判断某对象是否可以被调用。

python中__call__()方法的作用其实是把一个类的实例化对象变成了可调用对象，也就是说把一个类的实例化对象变成了可调用对象，只要类里实现了__call__()方法就行。如当类里没有实现__call__()时，此时的对象p 只是个类的实例，不是一个可调用的对象，当调用它时会报错：‘Person’ object is not callable.
```py
class People(object):
    def __init__(self,name):
        self.name=name

    def __call__(self):
        print("hello "+self.name)

a = People('无忌！')
a.__call__()       # 调用方法一
a()                # 调用方法二
```
输出
```py
hello 无忌！
hello 无忌！
```

## __str__方法
python的__str__()是一个特殊方法，它允许自定义对象的字符串表示形式。

使用__str__()方法可以提高代码的可读性和调试过程。它允许自定义对象的字符串表示，使其更容易理解。而不使用__str__()时，将得到默认的字符串表示，通常不够明确。

不使用__str__方法
```py

class Student(object):
    def __init__(self,id,name,age):
        self.id=id
        self.name=name
        self.age=age
 
s=Student(111,"Bob",18)
print(s)
```
输出结果：<main.Student object at 0x0362EBF0>

使用__str__方法
```py

class Student(object):
    def __init__(self,id,name,age):
        self.id=id
        self.name=name
        self.age=age
 
    def __str__(self):
        return "学号:{}--姓名:{}--年龄{}".format(self.id,self.name,self.age)
    
s=Student(111,"Bob",18)
print(s)
```
输出结果：学号:111--姓名:Bob--年龄18

## 如何调用父类（super）

# 类方法，实例方法，静态方法
## 实例方法
通常情况下，在类中定义的方法默认都是实例方法

实例方法最大的特点就是，它最少也要包含一个 self 参数，用于绑定调用此方法的实例对象（Python 会自动完成绑定）。实例方法通常会用类对象直接调用

Python 也支持使用类名调用实例方法，但此方式需要手动给 self 参数传值

## 类方法
Python 类方法和实例方法相似，它最少也要包含一个参数，只不过类方法中通常将其命名为 cls，Python 会自动将类本身绑定给 cls 参数（注意，绑定的不是类对象）。也就是说，我们在调用类方法时，无需显式为 cls 参数传参。

和实例方法最大的不同在于，类方法需要使用＠classmethod修饰符进行修饰

类方法推荐使用类名直接调用，当然也可以使用实例对象来调用（不推荐）

## 静态方法
静态方法，其实就是我们学过的函数，和函数唯一的区别是，静态方法定义在类这个空间（类命名空间）中，而函数则定义在程序所在的空间（全局命名空间）中。

静态方法没有类似 self、cls 这样的特殊参数，因此 Python 解释器不会对它包含的参数做任何类或对象的绑定。也正因为如此，类的静态方法中无法调用任何类属性和类方法。

静态方法需要使用＠staticmethod修饰

静态方法的调用，既可以使用类名，也可以使用类对象

## 类方法和静态方法的区别

1、类方法用在模拟java定义多个构造函数的情况。 由于Python类中只能有一个初始化方法，不能按照不同的情况初始化类。
```py
class Book(object):

    def __init__(self, title):
        self.title = title

    @classmethod
    def create(cls, title):
        book = cls(title=title)
        return book

book1 = Book("python")
book2 = Book.create("python and django")
print(book1.title)
print(book2.title)
```
特别说明，静态方法也可以实现上面功能，但静态方法每次都要写上类的名字，不方便。

2、类中静态方法方法调用静态方法的情况。
下面的代码，静态方法调用另一个静态方法，如果改用类方法调用静态方法，可以让cls代替类，
让代码看起来精简一些。也防止类名修改了，不用在类定义中修改原来的类名。


8.Python多线程实现方式

# search和match
均为re模块中的方法，用于正则表达式的匹配。

search()方法从整个字符串中搜索第一个匹配的子串，不限制搜索的起始位置。
match()方法从字符串的开头开始匹配，只在字符串开头找到匹配的子串。

# 垃圾回收
引用计数机制为主，标记-清除和分代回收机制为辅的策略。其中，标记-清除机制用来解决计数引用带来的循环引用而无法释放内存的问题，分代回收机制是为提升垃圾回收的效率。

# pass语句的作用
简单而言，pass 是一种空操作（null operation），解释器执行到它的时候，除了检查语法是否合法，什么也不做就直接跳过。它不会改变程序的执行顺序。它就像我们写的注释，除了占用一行代码行，不会对所处的作用域产生任何影响。

## 1、对人：作为空间占位符
我把它看作是一种言简意赅的注释方式，等于是说“这里先预留位置，回头再补上具体的代码实现”。

但是，若作为一种注释方式，它就显得太单薄了，比不上写“# todo: xxxx”，后者也会被 IDE 用颜色突显，而且意思更明确。虽然写起来简单，但它也引入了一个看似多余的关键字 pass。

所以，从空间占位符的角度来看，pass 不是编程语言中必须的设计要素。
## 2、对机器：为了语法完整性
对于前一条的用法，pass 出现在代码中的位置在理论上是不受限的。

但是，我们最常使用 pass 时，基本是在冒号的下一行，而且在该层缩进的代码块中，只有这一条语句。（参见前文的 3 个例子，为了方便，我们仅以以空函数为例）

如果不写它，会怎样？

答案是会报缩进错误：IndentationError: expected an indented block

因为 Python 使用缩进来划分代码块（至于原因，请查阅《Python为什么使用缩进来划分代码块？》），而冒号标识着要出现新的缩进代码块，所以这个例子会报缺少缩进代码块。

如果我们用前文说的注释来替代，也会报错：IndentationError: expected an indented block

原因是注释并非有效的语法内容，它会被 Python 解释器忽略掉（ignore），不像 pass 语句那样是“有效的语法内容，但是跳过”。


# python区分大小写吗
区分的。大写字母定义的变量而小写字母定义的同名变量不是同一个变量

# Python的Magic Method
# 变量__name__的含义
* name是一个变量，前后加了双下划线是因为这是系统定义的名字（python中系统变量都是双下划綫开头结尾），普通变量不使用这种命名方式；
* python有很多模块，这些模块是可以独立运行的（这一点与C语言和C++的头文件不同）；
* name是用来标识模块名字的一个系统变量。这里分两种情况：第一种情况指的是当前运行的模块，那么当前模块__main__ 的值就为__main__；第二种情况指的是该模块是使用import导入的模块，那么这个被导入模块的name变量的值为该模块的文件名（去掉.py）。

在__name__ 变量的帮助下，你可以判断出这时代码是被直接运行，还是被导入到其他程序中去了。


# Dict和List查询的效率差别及原因
dict的本质就是 hash 表，hash 表就是通过 key 找到其 value ，平均情况下你只需要花费 O(1) 的时间复杂度即可以完成对一个元素的查找查询的时间

而list底层是长度可变的数组，查询的时间复杂度为O(n)。

# Django请求的流程
![](https://img-blog.csdnimg.cn/img_convert/dea87717a86daefba7cb8f1aa5de6b65.png)

最重要的是回答用户请求并不是一下子通过URL匹配就达到相应视图，返回数据也不是一下子就返回给用户，中间要经历层层中间件。这个面试题其实考的核心是中间件。
# Django的中间件了解吗
# python类的内置方法有哪些，调用顺序如何，什么作用？
__new__ 和 __init__
__call__
__iter__ 和 __next__
__del__
__str__ 和 __repr__
__getattr__
__getattribute__
# 异常捕获
![](https://pic3.zhimg.com/80/v2-24efb932d899b530216f5192412ec61a_1440w.webp)
## 1 捕获所有异常
包括键盘中断和程序退出请求（用 sys.exit() 就无法退出程序了，因为异常被捕获了），因此慎用。
```py
try:
    <语句>
except:
    print('异常说明')
```

## 2 捕获指定异常
```py
try:
    <语句>
except <异常名> as e:
    print('异常说明')
```
万能异常：
```py
try:
    <语句>
except Exception as e:
    print('异常说明')
```

## 3 捕获多个异常
捕获多个异常有两种方式，第一种是一个 except 同时处理多个异常，不区分优先级：
```py
try:
    <语句>
except (<异常名1>, <异常名2>, ...):
    print('异常说明')
```
第二种是区分优先级的：
```py
try:
    <语句>

except <异常名1>:

    print('异常说明1')

except <异常名2>:

    print('异常说明2')

except <异常名3>:

    print('异常说明3')
```
该种异常处理语法的规则是：

执行 try 下的语句，如果引发异常，则执行过程会跳到第一个 except 语句。
如果第一个 except 中定义的异常与引发的异常匹配，则执行该 except 中的语句。
如果引发的异常不匹配第一个 except，则会搜索第二个 except，允许编写的 except 数量没有限制。
如果所有的 except 都不匹配，则异常会传递到下一个调用本代码的最高层 try 代码中。
## 4 异常中的 else
如果判断完没有某些异常之后还想做其他事，就可以使用下面这样的 else 语句。
```py
try:
　　<语句>
except <异常名1>:
　　print('异常说明1')
except <异常名2>:
　　print('异常说明2')
else:
　　<语句> # try语句中没有异常则执行此段代码
```
## 5 异常中的 finally
try…finally…语句无论是否发生异常都将会执行最后的代码。
```py
try:
　　<语句>
finally:
　　<语句>
```
看一个示例：
```py
str1 = 'hello world'
try:
　　int(str1)
except IndexError as e:
　　print(e)
except KeyError as e:
　　print(e)
except ValueError as e:
　　print(e)
else:
　　print('try内没有异常')
finally:
　　print('无论异常与否,都会执行我')
```
## 6 raise 主动触发异常
可以使用 raise 语句自己触发异常，raise 语法格式如下：
```py
raise [Exception [, args [, traceback]]]
```
语句中 Exception 是异常的类型（例如 ValueError），参数是一个异常参数值。该参数是可选的，如果不提供，异常的参数是 "None"。最后一个参数是跟踪异常对象，也是可选的（在实践中很少使用）。

看一个例子：
```py
def not_zero(num):
　　try:
　　　　if num == 0:
　　　　　　raise ValueError('参数错误')
　　　　return num
　　except Exception as e:
　　　　print(e)
not_zero(0)
```
# 垃圾回收
python类的内置方法有哪些，调用顺序如何，什么作用？
异常捕获
垃圾回收
# restful api的规范
## 路径
路径又称为端点，表示API的具体地址。在路径的设计中，需遵守下列约定：

* 命名必须全部小写
* 资源（resource）的命名必须是名词，并且必须是复数形式
* 如果要使用连字符，建议使用‘-’而不是 ‘ _ ’，‘ _ ’字符可能会在某些浏览器或屏幕中被部分遮挡或完全隐藏
* 易读。

为什么命名必须是名词且需要复数形式呢？这是因为在RESTful中，主语是资源，资源肯定是名词，不能是动词。其次，一个资源往往对应数据库中一张表，表就是实体的集合，因此需要是复数形式。
## HTTP动词
对于如何操作资源，有相应的HTTP动词对应，常见的动词有如下五个（括号里表示SQL对应的命令）：

GET（SELECT）：从服务器取出资源（一项或多项）
POST（CREATE）：在服务器新建一个资源
PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）
PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）
DELETE（DELETE）：从服务器删除资源
## 过滤
如果数据量很大，服务器不可能将全部数据都返回给前端，因此前端需要提供一些参数进行过滤，用于分页展示或者排序等，下面是一些常见的参数：

?limit=10：指定返回记录的数量
?offset=10：指定返回记录的开始位置。
?page=2&per_page=100：指定第几页，以及每页的记录数。
?sortby=name&order=asc：指定返回结果按照哪个属性排序，以及排序顺序。
?animal_type_id=1：指定筛选条件


# python如何异步？有没有使用过异步？


# is == 区别
is 的作用是用来检查对象的标示符是否一致，也就是比较两个对象在内存中的地址是否一样，而 == 是用来检查两个对象的值是否相等

我们在检查 a is b 的时候，其实相当于检查 id(a) == id(b)。而检查 a == b 的时候，实际是调用了对象 a 的 __eq()__ 方法，a == b 相当于 a.__eq__(b)

如果 a is b 返回True的话，即 a 和 b 指向同一块内存地址的话，a == b 也返回True，即 a 和 b 的值也相等

这里还有一个问题，为什么 a 和 b 都是 "hello" 的时候，a is b 返回True，而 a 和 b都是 "hello world" 的时候，a is b 返回False呢？

这是因为前一种情况下Python的字符串驻留机制起了作用，当字符串中出现了非标识符允许的字符的时候才不采取驻留，如果你把"hello world"改成"hello_world"， a is b还是返回 true，只是因为字符中有一个空格所以才不采用驻留，为了提高系统性能Python会保留其值的一个副本，当创建新的字符串的时候直接指向该副本即可。所以 "hello" 在内存中只有一个副本，a 和 b 的 id 值相同，而 "hello world" 有空格，为非标识符允许的字符，不驻留内存，Python中各自创建了对象来表示 a 和 b，所以他们的值相同但 id 值不同。
# Lambda 讲一下
函数式编程思想的体现，同时也是Python中创建匿名函数的方法，方便单次使用的函数的创建，它可以具有任意数量的参数，但只能有一个表达式。
6. post 有什么类型
# 数字转字符串方法
str()

format()

f-string

# 用过python哪些包
json
torch
django
transformers
requests：发送网络请求

# python多线程的缺点
由于全局解释器锁的存在，GIL导致PYTHON 无法使用到计算机的多核，仅能使用单核

如果是IO密集型应用，可以采用多进程+协程的方式
# 线程和协程的区别
线程是操作系统中任务调度的基本单位，线程切换需要从用户进入内核态再返回用户态

协程是比线程更小的单位，相当于用户级别的线程，一个线程内可以包含多个协程，协程切换不需要进入内核态

一个线程内的多个协程是串行执行的，不能利用多核，所以，显然，协程不适合计算密集型的场景。协程适合I/O 密集型任务。
# 文件操作（打开、修改、保存）使用什么方法
open(,'r')
open(,'w')
open(,'a')
f.read
f.write
close()
# 删除字典中的值用什么方法
del dict[key]

dict.pop(key)

# python线程和线程组


# python内存管理（内存池，垃圾回收机制，不了解的赶紧去查，高频）


# Python 的 list 去重
利用set和元素在原有list中的索引排序
```py
li=[1,2,3,4,5,1,2,3]
new_li=list(set(li))
new_li.sort(key=li.index)
print(new_li)
```

# 合并列表
```python
list1=[1,2,3]
list2=[4,5,6]
```

1. 直接使用"+"号合并列表
2. extend方法，会改变原有列表
3. 使用切片:
```python
list1[len(list1):len(list1)]=list2
```

# 传统方法实现单例模式
```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

# 装饰器实现单例模式
## 为类加装饰器
为类加装饰器的效果可能是修改类属性，修改类方法等。
### 修改类属性的类装饰器
```py
def decorater(cls):             # 传入一个类即cls
    cls.num_of_animals = 10     # 设置一个类属性
    return cls                  # 返回这个被装饰过的类

@decorater
class animal:
    pass
# 这就完成了对类的装饰啦

A = animal()  
# 上面这行代码相当于在运行a = decorater(animal) 运行的结果
# 就是返回了一个被装饰过的新的cls，因此新的cls有了新的属性，我们就可以调用
# 这个num_of_animals的属性啦。
```
### 设置类方法的装饰器
```py
def decorater(func):         
    def wrapper(cls):
        cls.num_of_animals = 10                   
        cls.f1 = func    
    	# 这里将传入的func即printd作为类的f1函数，我还不清楚怎么设置有self传入的函数。也可能不行
        return cls
    return wrapper

@decorater(printd)
class animal:
    pass

def printd(*args):
    print('this is a function')
    
A = animal()
A.f1()   # 是可以调用的哦
# 运行结果：this is a function
```
### 重写类的装饰器
也可以完全重写一个类
```py
def decorater(cls):
	class wrapper:
		pass     # 这里面可以重写类
	return wrapper
	
@decorater
class animal:
	pass
# 这样是可以的，但是一般来说是没必要这样写哈。
```

## 2 类装饰器实现单例模式
```py
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class MyClass:
    def __init__(self):
        pass

# 使用
instance1 = MyClass()
instance2 = MyClass()

print(instance1 is instance2)  # 输出: True
```

# 装饰器
```py
def my_fun(message)
    print(f'Hello! {message}')

my_fun('Jack')

def decorator(fn):
    def wrapper(*args,**kwargs):
        print('Func start')
        result = fn(*args,**kwargs)
        print('Func end')
        return result
    return wrapper

f1 = decorator(my_fun)
f1()
```