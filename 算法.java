public class 算法{

    int[] a=new int[]{4,1,3,5,8,7};
    // 冒泡排序
    void bubbleSort(int[] a){
        for(int i=0;i<a.length;i++){
            for(int j=1;j<a.length-i;j++){
                if(a[j]>a[j-1]){
                    int temp=a[j];
                    a[j]=a[j-1];
                    a[j-1]=temp;
                }
            }
        }
    }
    // 直接插入排序
    void insertSort(int[] a){
        for(int i=1;i<a.length;i++){
            int low=a[i];
            int leftIndex=i;
            while(leftIndex-1>=0&&a[leftIndex-1]>low){
                a[leftIndex]=a[leftIndex-1];
                leftIndex--;
            }
            a[leftIndex]=low;
        }
    }
    // 选择排序
    void selectSort(int[] a){
        for(int i=0;i<a.length;i++){
            int low=i;
            for(int j=i+1;j<a.length;j++){
                if(a[j]<a[low]){
                    low=j;
                }
            }
            if(low!=i){
                int temp=a[low];
                a[low]=a[i];
                a[i]=temp;
            }
        }
    }
    // 快速排序
    void quickSort(int[] a,int low,int high){
        if(low>high){
            return;
        }
        int i=low,j=high,k=a[low];
        while(i<j){
            while(i<j&&a[j]>k){
                j--;
            }
            while(i<j&&a[i]<=k){
                i++;
            }
            if(i<j){
                int temp=a[i];
                a[i]=a[j];
                a[j]=temp;
            }
        }
        a[low]=a[i];
        a[i]=k;
        quickSort(a, low, i-1);
        quickSort(a, i+1, high);
    }
    // 归并排序
    void mergeSort(int[] a,int low,int high,int[] temp){
        if(low>=high){
            return;
        }
        int mid=(low+high)/2;
        mergeSort(a, low, mid, temp);
        mergeSort(a, mid+1, high, temp);
        merge(a,low,mid,high,temp);
    }
    void merge(int[] a,int low,int mid,int high,int[] temp){
        int i=0,j=low,k=mid+1;
        while(j<=mid&&k<=high){
            if(a[j]<=a[k]){
                temp[i++]=a[j++];
            }
            else{
                temp[i++]=a[k++];
            }
        }
        while(j<=mid){
            temp[i++]=a[j++];
        }
        while(k<=high){
            temp[i++]=a[k++];
        }
        for(int k=0;k<i;k++){
            a[low+k]=temp[k];
        }
    }
}