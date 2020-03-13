<!-- 给定字符串 str，检查其是否符合美元书写格式
    1、以 $ 开始
    2、整数部分，从个位起，满 3 个数字用 , 分隔
    3、如果为小数，则小数部分长度为 2
    4、正确的格式如：$1,023,032.03 或者 $2.03，错误的格式如：$3,432,12.12 或者 $34,344.3 );   -->
<!--  没有考虑  除数字，"."和"$" 之外的情况-->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>xiaym的js演示程序</title>
</head>
<body>
<script>
    function isUSD(usd) {
        part = usd.split(".");
        if (part[1].length != 2) { //判断小数部分
            return false;
        } else {
            IntegerPart = part[0].split(",");
            for (i = 1; i < IntegerPart.length; i++) {  //判断 整数部分第二个开始的长度是否为3
                if (IntegerPart[i].length != 3) {
                    return false;
                }
                if (IntegerPart[0].length > 4 || IntegerPart[0].length < 1) { //判断 整数部分第一个长度是2到4之间
                    return false;
                }
                if (IntegerPart[0][0] != '$' || IntegerPart[0][1] == '0') { //判断 整数部分第一个的第一个字符不能是$和0
                    return false;
                }

            }
            return true;
        }

    }

    document.write('$20,933,209.93' + "<br>");
    document.write(isUSD('$20,933,209.93') + "<br>");

    document.write('$20,933,09.93' + "<br>");
    document.write(isUSD('$20,933,09.93') + "<br>");

    document.write('$2000,933,09.93' + "<br>");
    document.write(isUSD('$2000,933,09.93') + "<br>");

    document.write('$,933,09.93' + "<br>");
    document.write(isUSD('$,933,09.93') + "<br>");

    document.write('2,933,09.93' + "<br>");
    document.write(isUSD('2,933,09.93') + "<br>");

    document.write('$0,933,209.93' + "<br>");
    document.write(isUSD('$0,933,209.93') + "<br>");

    document.write('$20,9334,209.93' + "<br>");
    document.write(isUSD('$20,9334,209.93') + "<br>");
</script>
</body>
</html>