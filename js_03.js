<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>xiaym的js演示程序</title>
</head>
<body>
<script>
    function sum(arr) {
        result=0;
        for (var i = 0; i < arr.length; i++) {
            result=result + arr[i];
        }
        return result;
    }

    document.write("功能：求数组的和。[1,3,3,3,4]" + "<br>");
    document.write(sum([1, 3, 3, 3, 4]) + "<br>");

</script>
</body>
</html>
