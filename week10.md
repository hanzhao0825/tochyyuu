## 进展
对于编译安卓并且安装perf失败了。

寻找方法，看到有人写了traceview文件的parser。拿过来发现不能用，读出来的数据都是乱的。

查别人的说法，有说是因为64位和32位的record格式不一样。

尝试把record长度由9位改到14位，成功读出数据。

搜索到一个perl的库，可以把输入文件转变成flamegraph.svg，正在研究如何使用