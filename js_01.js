<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>xiaym的js演示程序</title>
</head>
<body>
<script>
    function indexOf(arr, item) {
        for (var i = 0; i < arr.length; i++) {
            if (arr[i] == item) {
                return i;
            }
        }
        return -1;
    }

    document.write("功能：查找数组中给定的值。[1,3,3,3,4],3" + "<br>");
    document.write(indexOf([1, 3, 3, 3, 4], 3) + "<br>");
    
</script>
</body>
</html>
