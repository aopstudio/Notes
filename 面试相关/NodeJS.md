# 闭包是什么？
能够访问另一个函数作用域中变量的函数。

闭包的主要作用：延伸了变量的作用范围

# promise
Promise 是 JavaScript 中用于异步编程的一个重要概念。一个 Promise 对象代表了一个可能现在、可能未来某个时候才会完成（或失败）的异步操作及其结果值。它允许你为异步操作的成功完成、失败或终止指定处理方法。

```javascript
const p = new Promise(function(resolve,reject){
    resolve('成功') 
    console.log(1);
    // reject('失败')
});
p.then(
    res=>{
        console.log(res,'res'); //成功时会走这个函数并且打印"成功"
    },
    err=>{
        console.log(err,'err'); //失败时会走这个函数并且打印"失败"
    }
);
```
## 事件循环
宏任务由宿主环境（Nodejs，浏览器）发起，比如setTimeout()；微任务由JS引擎发起，主要有promise

1. 同步代码（js执行栈）
2. 微任务的异步代码（js引擎）
    * Promise.then() catch()    Promise本身里面的代码是同步任务代码，但then和catch属于异步任务中的微任务
    * async/await
    * Object.observe()
3. 宏任务的异步代码（宿主环境）
    * 代码块（所有的代码是一个大的宏任务）
    * setTimeout()
    * IO
### 执行顺序
1. 同步任务直接放到执行栈中，由主线程执行。

2. 异步任务放到宿主环境中

3. 异步任务满足执行条件时，微任务放到微任务队列，宏任务放到宏任务队列

4. 执行栈执行完毕后，先去微任务队列看有没有，按顺序执行

5. 微任务队列执行完毕后，去宏任务队列看有没有，按顺序执行

## 基本概念
* Pending（待定）: 初始状态，既不是成功，也不是失败。
* Fulfilled（已兑现）: 意味着操作成功完成。
* Rejected（已拒绝）: 意味着操作失败。
## 核心 API
### Promise 构造函数: new Promise(executor)

executor 是带有 resolve 和 reject 两个参数的函数。executor 函数是由 Promise 的构造函数执行的。
resolve 函数在异步操作成功时调用，并将异步操作的结果，作为参数传递出去。
reject 函数在异步操作失败时调用，并将异步操作的错误，作为参数传递出去。
### Promise.prototype.then(onFulfilled, onRejected)

添加兑现（onFulfilled）和拒绝（onRejected）回调到当前 Promise，并返回一个新的 Promise，以链式调用。
onFulfilled 是 Promise 成功时的回调。
onRejected 是 Promise 失败时的回调。
### Promise.prototype.catch(onRejected)

添加一个拒绝（失败）回调到当前 Promise，等同于 .then(null, onRejected)。
### Promise.prototype.finally(onFinally)

添加一个事件处理回调，无论 Promise 是成功还是失败，都会执行该回调。

# git
一些最主要的 Git 命令：

* git init: 在当前目录中初始化一个新的 Git 仓库。
* git clone [url]: 克隆（即复制）一个仓库到新的目录中。
* git add [file]: 将文件添加到暂存区，准备进行提交。
* git commit -m "[commit message]": 将暂存区的更改提交到仓库中。每次提交都会有一个相关的提交信息，描述了进行更改的原因。
* git status: 显示工作目录和暂存区的状态，如哪些文件被修改但未提交。
* git push [alias] [branch]: 将本地分支的更新推送到远程仓库。
* git pull [alias] [branch]: 从远程仓库拉取最新的版本到本地并自动合并。
* git branch: 列出、创建或删除分支。
* git checkout [branch-name]: 切换到指定的分支。
* git merge [branch]: 将指定分支的历史合并到当前分支。
* git log: 显示提交历史记录。
* git diff: 显示工作目录和索引（或两个提交）之间的差异。

# Hashmap的原理
哈希函数+链表



# 事件循环
## 宏任务有什么，微任务有什么

# React
虚拟DOM，直接操作DOM过于繁琐
## 三大特点
### 组件（Component）
其核心思想基于一个简单的策略：分而治之。如果一个问题作为一个整体很难理解透彻和解决，我们就把它拆分为多个小问题，各个击破，最后再将结果综合起来

React 组件有两条重要的属性：
1. 组件是可组合的（composable）。组件的目的在于重用，我们可以使用现有组件创建新组件。
2. 一个组件独立于其它组件（independent）。当修改一个组件时，不相干的组件不会受到干扰。

### 声明式界面编程（Declarative UI）
用技术术语来讲，如果一段代码定义的是如何做一件事的步骤，我们称之为命令式；相反，如果定义的是我们所预期的最
终结果，它就是声明式。直接操作 DOM API 的传统 web 开发方式是命令式，而 React 是声明式。

### 响应式 DOM 更新机制（Reactive DOM updates）
我们写程序时只需要将该数据与相应界面元素关联好，就不需要再做任何后续干涉。当数据发生变化时，React 将自动对相关 DOM 元素做相应的调整。这样看起来就像是 DOM 响应了数据变化（的号召）而自发地做出更改，我们并不需要手动跟踪数据的变化，也不需要担心何时去更改 DOM（实质上是 React代劳）。这就是响应式（reactive）界面开发方法
## 钩子函数
* useState
在函数组件中使用有状态值

state 和 props的区别
State是我们可以在React组件中读取和更新的值。
Props是传递给React组件的值，并且是只读的(它们不应该被更新)。
* useEffect
纯函数只能进行数据计算，不涉及计算的操作（比如生成日志、储存数据、改变应用状态等等）就是副作用。useEffect里面就用来写执行副作用的代码。

如果不写第二个参数，组件每渲染一次，该函数就自动执行一次

有时候，我们不希望useEffect()每次渲染都执行，这时可以使用它的第二个参数，使用一个数组指定副效应函数的依赖项，只有依赖项发生变化，才会重新渲染。
* useCallback
useContext提供了一种比使用标准context更简单的使用上下文的方式。消费者的组件。
语法包括将我们想要使用的整个Context对象传递给useContext。返回值是传递给Context的值。

# Promise

# 事件循环



# 强制缓存和协商缓存
1. 强制缓存
用户请求数据，如果命中了缓存且缓存没有失效，则不向服务端请求数据，而直接从本地资源获取。

用户请求数据，如果命中了缓存且缓存失效，会向服务器重新请求资源，数据喝资源返回后，再次根据缓存规则存入浏览器缓存。

那么浏览器是怎么判断缓存是否失效呢？
强制缓存的response header中有两个字段表明失效规则（Expires/ Cache-Control）;


1.1 Expires：Expires的值为服务端返回的到期时间，即下一次请求时，请求时间小于服务端返回的到期时间，直接使用缓存数据。不过Expires 是HTTP 1.0的东西，现在默认浏览器均默认使用HTTP 1.1，所以它的作用基本忽略。另一个问题是，到期时间是由服务端生成的，但是客户端时间可能跟服务端时间有误差，这就会导致缓存命中的误差。 所以HTTP 1.1 的版本，使用Cache-Control替代。


1.2 Cache-Control：Cache-Control 是最重要的规则。常见的取值有private、public、no-cache、max-age、no-store;

2. 协商缓存
用户请求数据，浏览器直接向服务器发送请求，协商对比服务器端和本地的资源，验证本地资源是否有效。

协商缓存一般是使用 if-modified-since/Last-Modified 和 if-none-match/Etag 由服务器来决定浏览器缓存的资源是否可以使用。

Last-Modified：服务器响应请求时，告诉浏览器资源最后的修改时间。
If-Modified-Since：浏览器再次请求资源时，浏览器通知服务器，上次请求时，返回的资源最后修改时间。
若最后修改时间小于等于If-Modified-Since，则response header返回304，告知浏览器继续使用所保存的cache。若大于If-Modified-Since，则说明资源被改动过，返回状态码200；


两类缓存规则可以同时存在，强制缓存优先级高于协商缓存，也就是说，当执行强制缓存的规则时，如果缓存生效，直接使用缓存，不再执行协商缓存规则。如果强制缓存规则不生效，则需要进行协商缓存判断。

# 数组
## 数组方法
### concat()
concat() 方法用于合并两个或多个数组。**此方法不会更改现有数组**，而是返回一个新数组。
```js
const array1 = ['a', 'b', 'c'];
const array2 = ['d', 'e', 'f'];
const array3 = array1.concat(array2);
console.log(array3);
```
### forEach()
只为每个数组元素调用一次函数。它不会返回一个新的或修改后的数组
```js
const array1 = ['a', 'b', 'c'];

array1.forEach((element) => element.toUpperCase());
```
### filter()
filter()方法创建一个新数组，其中包含对原始数组中的每个元素调用提供的回调函数后返回 true 的元素。它返回一个由通过筛选的元素组成的新数组
### every()
every()方法检查数组中的每个元素是否满足提供的测试函数，如果所有元素都返回 true，则返回 true；否则，返回 false
### some()
some()方法检查数组中的每个元素是否至少有一个满足提供的测试函数，如果有至少一个元素返回 true，则返回 true；否则，返回 false。
### join()
join() 方法将一个数组（或一个类数组对象）的所有元素连接成一个字符串并返回这个字符串
```js
const elements = ['Fire', 'Air', 'Water'];

console.log(elements.join());
// Expected output: "Fire,Air,Water"

console.log(elements.join(''));
// Expected output: "FireAirWater"

console.log(elements.join('-'));
// Expected output: "Fire-Air-Water"
```
### push()
向数组末尾添加新元素，**会改变数组本身**
### pop()
从数组末尾弹出一个元素，**会改变数组本身**
### unshift()
向数组开头添加新元素，**会改变数组本身**
### shift()
从数组开头弹出一个元素，**会改变数组本身**
### reverse()
reverse() 方法就地反转数组中的元素，并返回同一数组的引用。数组的第一个元素会变成最后一个，数组的最后一个元素变成第一个。换句话说，数组中的元素顺序将被翻转，变为与之前相反的方向。
**会改变数组本身**

### slice()
slice() 方法返回一个新的数组对象，这一对象是一个由 start 和 end 决定的原数组的浅拷贝（包括 start，不包括 end），其中 start 和 end 代表了数组元素的索引。原始数组不会被改变。类似于Python的切片

### sort()
sort() 方法就地对数组的元素进行排序，并返回对相同数组的引用。默认排序是将元素转换为字符串，然后按照它们的 UTF-16 码元值升序排序。
**会改变数组本身**

### splice()
splice() 方法通过移除或者替换已存在的元素和/或添加新元素就地改变一个数组的内容。
**会改变数组本身**

```js
const months = ['Jan', 'March', 'April', 'June'];
months.splice(1, 0, 'Feb');
// Inserts at index 1
console.log(months);
// Expected output: Array ["Jan", "Feb", "March", "April", "June"]

months.splice(4, 1, 'May');
// Replaces 1 element at index 4
console.log(months);
// Expected output: Array ["Jan", "Feb", "March", "April", "May"]
```

splice(start, deleteCount, item1)
#### 参数
* start:
从 0 开始计算的索引，表示要开始改变数组的位置

* deleteCount 可选
一个整数，表示数组中要从 start 开始删除的元素数量。
**如果省略了 deleteCount**，或者其值大于或等于由 start 指定的位置到数组末尾的元素数量，那么从 start 到数组末尾的所有元素将被删除

* item1, …, itemN 可选
从 start 开始要加入到数组中的元素。
如果不指定任何元素，splice() 将只从数组中删除元素。

## HTTP1.0 HTTP 1.1主要区别

### 1.1 长链接

HTTP 1.0需要使用keep-alive参数来告知服务器端要建立一个长连接，而HTTP1.1默认支持长连接。

HTTP是基于TCP/IP协议的，创建一个TCP连接是需要经过三次握手的,有一定的开销，如果每次通讯都要重新建立连接的话，对性能有影响。因此最好能维持一个长连接，可以用个长连接来发多个请求。
### 1.2 节约带宽

HTTP 1.1支持只发送header信息(不带任何body信息)，如果服务器认为客户端有权限请求服务器，则返回100，否则返回401。客户端如果接受到100，才开始把请求body发送到服务器。

这样当服务器返回401的时候，客户端就可以不用发送请求body了，节约了带宽。

另外HTTP还支持传送内容的一部分。这样当客户端已经有一部分的资源后，只需要跟服务器请求另外的部分资源即可。这是支持文件断点续传的基础

### 1.3 支持HOST域
HTTP1.0是没有host域的，HTTP1.1才支持这个参数。

由于HTTP 1.0不支持Host请求头字段，WEB浏览器无法使用主机头名来明确表示要访问服务器上的哪个WEB站点，这样就无法使用WEB服务器在同一个IP地址和端口号上配置多个虚拟WEB站点。

在HTTP 1.1中增加Host请求头字段后，WEB浏览器可以使用主机头名来明确表示要访问服务器上的哪个WEB站点，这才实现了在一台WEB服务器上可以在同一个IP地址和端口号上使用不同的主机名来创建多个虚拟WEB站点。

## HTTP1.1与HTTP 2.0的主要区别 
HTTP2.0采用二进制传输数据，采用多路复用，压缩了报文头部，客户端在发起请求后服务器可以主动向客户端推送相关的资源，更加安全
### 多路复用
多路复用允许同时通过单一的http/2 连接发起多重的请求-响应消息。 有了新的分帧机制后，http/2 不再依赖多个TCP连接去实现多流并行了。 每个数据流都拆分成很多互不依赖的帧，而这些帧可以交错（乱序发送），还可以分优先级，最后再在另一端把它们重新组合起来。 http 2.0 连接都是持久化的，而且客户端与服务器之间也只需要一个连接（每个域名一个连接）即可。 http2连接可以承载数十或数百个流的复用，多路复用意味着来自很多流的数据包能够混合在一起通过同样连接传输。
### 二进制分帧
将数据分割为更小的帧，通过多路复用在同一个连接上发送和接收多个帧，提高了传输的效率。
### 首部压缩
使用HPACK算法对请求/响应的头部进行压缩，减少了数据传输的大小。
### 服务器推送
服务器可以主动向客户端推送资源，减少了客户端发起请求的次数。

## HTTP 3:
* 使用QUIC作为传输协议：HTTP 3基于QUIC（Quick UDP Internet Connections）协议，取代了TCP作为传输层协议。
* 改进的拥塞控制：HTTP 3使用了更先进的拥塞控制算法，提高了网络的稳定性和性能。
* 减少握手延迟：QUIC协议通过0-RTT（零往返时间）握手和快速握手恢复，减少了握手的延迟。
* 抗丢包能力：QUIC协议具有更好的丢包恢复能力，可以更快地恢复丢失的数据包。