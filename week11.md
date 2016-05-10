## 进展
编写了parse.py，可以对安卓DDMS生产的trace文件进行解析，并且得到中间文件。

然后交给一个基于perl的FlameGraph的库：https://github.com/brendangregg/FlameGraph，生产svg文件

比如，我先拿我之前自己的那个程序测试，讲my.trace生成my.result，然后生成my.svg

均在本目录下，可以用浏览器打开