
```
  _____         _                         _   
 |_   _|       | |                       | |  
   | |   _ __  | |_  ___  _ __  ___  ___ | |_ 
   | |  | '_ \ | __|/ _ \| '__|/ _ \/ __|| __|
  _| |_ | | | || |_|  __/| |  |  __/\__ \| |_ 
 |_____||_| |_| \__|\___||_|   \___||___/ \__|
```                                             
[↑ here](http://patorjk.com/software/taag/)    
[❤](https://emojipedia.org/)    
# Interest

## brickout
是一个简单的打砖块的游戏. 基于 `pygame` .后来加了一个开始、结束界面.       
用鼠标后者方向键控制挡板的左右移动.      
![brick](/brickout/brickout.PNG)

基于[geekcomputers](https://github.com/geekcomputers/Python/tree/master/brickout-game).

## snake
稍稍熟悉一点 `pygame` 后， 完成了贪吃蛇游戏. 相比于打砖块，这个要更加完整一些. 加入了暂停和加速功能.        
方向键控制贪吃蛇的移动，enter 键暂停游戏，连击方向键会加速移动.     
![snake](/snake/snake.PNG)

## CharacterVideo
使用 `opencv` 读取视频，将每帧图片转为灰度图. 再映射到相应字符.      
不过在 windows 上效果不太好.

## splicePicture
目标图片    
![jj](/Interest/splicePicture/jj.jpg)

### splice
splice.py 给定一组图片，按照像素分布将其填充为目标图片.       
![splice](/Interest/splicePicture/new.png)

### splice9
splice9.py 将目标图片扩展为正方形图片，然后将其切为九张，保存到指定目录.

### square
square.py 将目标图片填充或切割为正方形.

### cluster
cluster.py 将目标图片的 RGB 值聚类，并将类簇的 RGB 平均值填充各类簇，以此得到一张新的图片.
类个数 k=3.     
![cluster](/Interest/splicePicture/k_new.png)

## clock
使用 `turtle` ，模拟表盘.
### hand_clock
模拟指针.       
![hand](/clock/hand_clock.PNG)

### digit_clock
模拟七段数码管.        
![digit](/clock/digit_clock.PNG)

## translator
基于[CharlesPikachu](https://github.com/CharlesPikachu/Tools/tree/master/Translator).     
后续使用 `tkinter` 加了图形界面，补充了百度翻译的双语示例.       
![translate](/translator/translate.PNG)

## chat

## nervousCat

