let a = [1,3,4,5,6,7,9]
let i=6
let left=0,right=a.length-1;
while(right>=left){
    let mid=Math.floor((left+right)/2)
    if(a[mid]==i){
        console.log(mid)
        return
    }
    if(a[mid]>i){
        right=mid-1
    }
    else{
        left=mid+1
    }
}
console.log(-1)