## 程序功能： 实现sort接口

import java.math.BigDecimal;
import java.util.Arrays;

public class sortMyTest {
    public static void main(String[] args) {
        Person[] ps = new Person[] {
                new Person("Bob", 61.5),
                new Person("Alice", 61.2),
                new Person("Lily", 75),
        };
        Arrays.sort(ps);
        System.out.println(Arrays.toString(ps));
    }
}

class Person implements Comparable<Person> {
    String name;
    double score;
    Person(String name, double score) {
        this.name = name;
        this.score = score;
    }
    @Override
    public int compareTo(Person other) {
        //这里每次new两个对象，如果数据量大，肯定是慢的。
        BigDecimal a = new BigDecimal(this.score);
        BigDecimal b = new BigDecimal(other.score);
      return a.compareTo(b);
    }
    @Override
    public String toString() {
        return this.name + "," + this.score;
    }
}
