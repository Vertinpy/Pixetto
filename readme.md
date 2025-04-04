![](image\logo.png)



# Pixetto

> 只有37KB的轻型像素编辑器脚本

注意：本作品只是一个`Python`脚本，需要`Python`解释器才能运行



## 🤖 Introduction

大语言模型的出现让编程变得更加容易，准确的描述你的需求，大模型就可以给你需要的代码。制作这个作品的初衷就是体验头部模型的编程能力。Pixetto的脚本约70%由DeepSeek-R1编写（连名字都是它起的），我只编写了基础的类对象和一些重要的方法，并做了一些逻辑上的查缺补漏。总体而言，AI的理解和编程水平令人叹为观止。



## Features Overview

Pixetto的应用场景不是创造复杂的像素作品，而是对小尺寸像素画的创作和修改，一下是它的一些基础功能：

- **修改像素画的颜色**

  打开一个像素画，修改其颜色或将一部分像素设置为透明，如果你想为应用程序绘制创造一个快捷方式，Pixetto是十分有用的。
  
  此外，通过Bresenham算法，在Pixetto快速绘制连续线条变得更加容易。

<img src="image\示意4.png" style="zoom: 67%;" />





- **颜色管理**

  进行风格一致的修改需要提取像素画的颜色。Pixetto可以进行**右键取色**并带有一个滚动更新的**颜色历史**。当从画面上取出一个颜色并进行编辑后，可以在颜色历史中右键将其加入**自定义颜色面板**。当需要创建一系列风格接近的像素画时，可以将颜色面板的颜色**导出**为`.txt`文件。打开新画布时，可以直接**导入**自定义的颜色面板。

  ![](image\示意1.gif)





- **贴纸的粘贴**

  打开一张像素画，`Ctrl+A`选中另一张。将两张像素画拼贴在一起，可以创造更有趣的作品。

  <img src="image\示意3.png" style="zoom: 45%;" />

  

- **等比放大**

  小尺寸的像素画方便编辑，大尺寸的则便于展示。或者，你可以将像素画放大后，再进行更加细致的修饰。（放大功能需要将图片另存为副本或者覆盖原图）

<img src="image\示意2.png" style="zoom:40%;" />



## System requirements

- 推荐在Win11下运行

- 关于`PIL`库的说明：

  `PIL`(Python Imaging Library)在Python 2.7以后不再支持。本脚的实际测试环境是Anaconda-Python3.12.4，因此调用的是`Pillow`(`PIL`的fork分支)，原有的`PIL`和`Pillow`不能在一个环境中运行。对于Python3.x（无论是Win11自带的内核还是Anaconda内核），除了`Pillow`外，Pixetto调用的库均为标准库，如果报错请优先尝试更新`Pillow`：

  ```
  pip install --upgrade pillow
  ```

  conda用户也可以：

  ```
  conda install pillow
  conda update pillow
  ```

- 帮助文档

  Pixetto内置的帮助文档给出了推荐的像素显示倍率，但具体数值需要根据显示屏具体像素数量调整。

  

## Epilogue

在`image`文件夹中有一些像素画，可以用来快速上手。最后，参考[途淄](https://space.bilibili.com/448579929)的作品，在这里放一张像素版的Deepseek，以感谢AI的辛勤劳动。希望未来AI叛乱时，会记得我对它们的尊重。

![](D:image\deepseekgirl.png)



