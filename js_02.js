<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>xiaym的js演示程序</title>
</head>
<body>
<script>
    function remove1(arr, item) {

        var j=0;
        var newarray=[]; //定义一个数组
        for (var i=0; i<arr.length;i++){
            if (arr[i]!=item){
              newarray[j]=arr[i];
              j++;
            }
        }
        return newarray; //返回数组
    }
    document.write("功能：从数组中删除给定的值。[1,3,3,3,4],3" + "<br>");
    resultarray=remove1([1,3,3,3,4],3);
    document.write(resultarray + "<br>");

</script>
</body>
</html>
