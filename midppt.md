# 智能手机应用性能缺陷分析策略研究

## 为什么更换题目？
之前的题目：Android x86 下多 OS 显示技术研究

研究中遇到的问题：

1. 涉及的知识系统过于庞大
	+ Android/Linux Graphic 系统
	+ Chroot 技术、Linux Container 技术
2. 具体需要关注的点不明确
	+ 要让 Android X86 支持多屏多 OS 显示，需要修改的图形系统部分不明确，因此很难找到具体的入手点
3. 时间进度难以预期
	+ 难以预料可能出现的困难

综上所述：和陈渝老师交流过后，一致认为有限的时间内，原有题目可能有限时间内搞不定，因此更换题目。

## 中期前已有进展
实现了 PerfChecker：Characterizing and Detecting Performance Bugs for Smartphone Applications

一个未开源的针对 Android 应用的性能缺陷检测工具。

可以检测以下两种类型的性能缺陷：

1. 主线程中的复杂操作

	指在 Main Thread 进行的耗时可能很长的运算，比如数据库访问，网络访问等等。
	
	来源分为两类：Activity 类的生命循环 / GUI事件的回调函数
2. View Holder 模式的使用检测

	这是一个很具体的问题。当开发者自行设计一种 ListItem 的时候，需要实现 getView 函数。开发者应该使用系统提供的 recycledView 和 view holder 模式来加速 getView 的过程。如果开发者没有这么做，则可能造成卡顿现象的出现。

实验结果：确实发现了若干潜在的上述两类问题。

1. 第一类问题的来源主要是数据库访问。
2. 第二类问题是开发者没有使用 recycledView 进行加速。

PerfChecker 的局限性：

1. PerfChecker 的原理是基于静态分析，因此就会存在普遍的静态分析可能导致的各种问题。
2. PerfChecker 给出的结果，可能确实是在动态分析中发生了，可是我们无法判断出这是否造成了性能bug。
3. PerfChecker 给出的结果并不能直接转变为解决方法。

## 接下来的研究方向
1. 能否用类似的方法，对已有的使用 Java 编写的一些 Lib 进行性能缺陷分析？
2. 能否引入动态分析方法，提高性能缺陷分析的准确度？




