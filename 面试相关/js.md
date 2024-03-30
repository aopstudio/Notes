# Promise
## Promise.all（全部成功或任意一个失败时返回）
Promise.all()方法用于将多个 Promise 实例，包装成一个新的 Promise 实例。

当所有输入的 Promise 都被兑现时，返回的 Promise 也将被兑现（即使传入的是一个空的可迭代对象），并返回一个包含所有兑现值的数组。如果输入的任何 Promise 被拒绝，则返回的 Promise 将被拒绝，并带有第一个被拒绝的原因。

```js
// test
let p1 = new Promise(function(resolve, reject) {
    setTimeout(function() {
        resolve(1)
    }, 1000)
})
let p2 = new Promise(function(resolve, reject) {
    setTimeout(function() {
        resolve(2)
    }, 2000)
})
let p3 = new Promise(function(resolve, reject) {
    setTimeout(function() {
        resolve(3)
    }, 3000)
})
Promise.all([p3, p1, p2]).then(res => {
    console.log(res) // [3, 1, 2]
})
```
## Promise.race （有一个改变状态（成功或失败）时返回）
race是竞赛赛跑的意思，竞赛肯定最受关注的就是第一名，其他的就无所谓了。

Promise.race()方法同样是将多个 Promise 实例，包装成一个新的 Promise 实例。
```js
const p = Promise.race([p1, p2, p3]);
```
上面代码中，只要p1、p2、p3之中有一个实例率先改变状态，p的状态就跟着改变。那个率先改变的 Promise 实例的返回值，就传递给p的回调函数。

例子
```py
const p = Promise.race([
  fetch('/resource-that-may-take-a-while'),
  new Promise(function (resolve, reject) {
    setTimeout(() => reject(new Error('request timeout')), 5000)
  })
]);
​
p
.then(console.log)
.catch(console.error);
```

如果指定时间内没有获得结果，就将 Promise 的状态变为reject，否则变为resolve。这也是fetch进行超时设置的原理。

## Promise.allSettled（全部改变状态（可以是成功也可以是失败）后返回）
Promise.allSettled()方法接受一个数组作为参数，数组的每个成员都是一个 Promise 对象，并返回一个新的 Promise 对象。只有等到参数数组的所有 Promise 对象都发生状态变更（不管是fulfilled还是rejected），返回的 Promise 对象才会发生状态变更。
```js
const promises = [
  fetch('/api-1'),
  fetch('/api-2'),
  fetch('/api-3'),
];
​
await Promise.allSettled(promises);
removeLoadingIndicator();
```

上面示例中，数组promises包含了三个请求，只有等到这三个请求都结束了（不管请求成功还是失败），removeLoadingIndicator()才会执行

该方法返回的新的 Promise 实例，一旦发生状态变更，**状态总是fulfilled，不会变成rejected**。状态变成fulfilled后，它的回调函数会接收到一个数组作为参数，该数组的每个成员对应前面数组的每个 Promise 对象。

```js
const resolved = Promise.resolve(42);
const rejected = Promise.reject(-1);
​
const allSettledPromise = Promise.allSettled([resolved, rejected]);
​
allSettledPromise.then(function (results) {
  console.log(results);
});
// [
//    { status: 'fulfilled', value: 42 },
//    { status: 'rejected', reason: -1 }
// ]
```
## Promise.any （任意一个成功或全部失败后返回）
Promise.any()主要是针对只要参数实例有一个变成fulfilled状态，包装实例就会变成fulfilled状态；如果所有参数实例都变成rejected状态，包装实例就会变成rejected状态。

Promise.any()不会因为某个 Promise 变成rejected状态而结束，必须等到所有参数 Promise 变成rejected状态才会结束。

### 返回值：

1. 只要其中的一个 promise 成功，就返回那个已经成功的 promise
2. 如果可迭代对象中没有一个 promise 成功（即所有的 promises 都失败/拒绝），就返回一个失败的 promise 和 AggregateError 类型的实例，它是 Error 的一个子类，用于把单一的错误集合在一起
### 例子1
```js
let p1 = new Promise(function (resolve, reject) {
    setTimeout(function () {
        resolve(1)
    }, 1000)
})
let p2 = new Promise(function (resolve, reject) {
    setTimeout(function () {
        resolve(2)
    }, 300)
})
let p3 = new Promise(function (resolve, reject) {
    setTimeout(function () {
        reject(3)
    }, 2000)
})
​
Promise.any([p1, p2, p3]).then(res => {
    console.log(res)//2
})
```
上面的Promise数组中有两个Promise实例状态是成功的，但any只返回最先成功的一个，这个和Promise.race方法有点类似，但race也可能返回最先失败的那个，而any只有等全部的都失败了才返回

### 例子2
那如果是全部失败呢？
```js
let p1 = new Promise(function (resolve, reject) {
    setTimeout(function () {
        reject(1)
    }, 1000)
})
let p2 = new Promise(function (resolve, reject) {
    setTimeout(function () {
        reject(2)
    }, 300)
})
let p3 = new Promise(function (resolve, reject) {
    setTimeout(function () {
        reject(3)
    }, 2000)
})
​
Promise.any([p1, p2, p3]).then(res => {
    console.log(res)
}).catch(err => {
    console.log(err);
})
```
看下结果：
```js
AggregateError: All promises were rejected
```
