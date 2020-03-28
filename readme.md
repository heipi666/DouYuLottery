# 某鱼弹幕抽奖脚本

## 使用步骤
1. 安装selenium
> pip install selenium
2. 安装chromeDriver
chromedriver的版本一定要与chrome的版本一致
在chrome浏览器中输入chrome://version/
### 下载地址
> http://npm.taobao.org/mirrors/chromedriver/
3. 解压压缩包，找到chromedriver.exe复制到chrome的安装目录。复制chromedriver.exe文件的路径并加入到电脑的环境变量中去
4. 配置config文件,输入弹幕抽奖的房间号,发言频率以及抽奖时间
5. python ./sendMsg.py执行
6. 第一次执行需要进行扫码登录，需要在20s内在弹出的浏览器网页进行扫码登录
7. 等待中奖, hhh!
