let arr=[{key:'key1',value:'value1'},{key:'key2',value:'value2'}]

function fn(arr){
    res = {}
    for(const obj of arr){
        const {key,value} = obj;
        res[key]=value
    }
    return res
}

console.log(fn(arr))

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function printSequentially() {
await delay(1000);
console.log(1);

await delay(1000);
console.log(2);

await delay(1000);
console.log(3);
}
  
printSequentially();
  
let str=['hello world']

function fn_str(str){
    let res = [];
    for(const s of str){
        res.push(s.split(' ').map(st=>st[0].toUpperCase()+st.slice(1)).join(' '))
    }
    return res
}
console.log(fn_str(str))