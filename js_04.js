<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>xiaym的js演示程序</title>
</head>
<body>
<script>
    function removeWithoutCopy(arr,item) {
        tmparray=[];
        j=0;
        for (var i = 0; i < arr.length; i++) {
            if (arr[i] != item){
                tmparray[j]=arr[i];
                j++;
            }
        }
        arr=[]; // 清除数组
        arr=tmparray; // 数组赋值
        return arr;
    }

    document.write("移除数组 arr 中的所有值与 item 相等的元素，直接在给定的 arr 数组上进行操作，并将结果返回。[1,3,3,3,4],3" + "<br>");
    document.write(removeWithoutCopy([1, 3, 3, 3, 4],3) + "<br>");

</script>
</body>
</html>
