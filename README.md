# 微博吃瓜神器

主要功能：实时获取微博热搜榜动态，主要检测tag为“爆”的热搜，以及热搜榜一和上升速度最快的热搜，并提供消息提示框提醒和shell提醒两种方式。（弹窗功能仅支持Win系统）

## 使用方法

```bash
weiboSpider> python .\BoomDetecter.py --help
usage: BoomDetecter.py [-h] [-d DELAY] [--duration DURATION] [-s] [-l] [--show-top {shell,notification,0,1}] [--trend {shell,notification,0,1}]
                       [--trend-threshold TREND_THRESHOLD]

A Weibo hotrank detecter

optional arguments:
  -h, --help            show this help message and exit
  -d DELAY, --delay DELAY
                        delay between two checks, seconds
  --duration DURATION   Duration of notification
  -s, --slient          Show notifications only in shell
  -l, --log             Show logs in shell
  --show-top {shell,notification,0,1}
                        Show the top topic. Shell or 0: show in shell; notification or 1: show in notifications
  --trend {shell,notification,0,1}
                        Show the fastest increase topic. Shell or 0: show in shell; notification or 1: show in notifications
  --trend-threshold TREND_THRESHOLD
                        Threshold of trend analyze

```

## Sample

- 基本功能：每60秒检测一次微博热搜榜有没有“爆”话题

```bash
weiboSpider> python .\BoomDetecter.py -d 60
```

运行后最小化命令行即可，一旦发现新的“爆”话题，即可右下角弹窗提示。

- 每120秒检测一次微博热搜榜有没有“爆”话题，仅显示在shell内，并检测热搜榜一内容，其中“爆”话题使用弹窗显示，热搜榜一内容仅显示在shell

```bash
weiboSpider> python .\BoomDetecter.py -d 120 --show-top shell --slient
```

- 每60秒检测一次微博热搜榜有没有“爆”话题，并检测距上次热搜榜中排名上升最快的话题，当上升最快的话题上升低于10名不显示，大于等于10名则显示在右下角提示框

```bash
weiboSpider> python .\BoomDetecter.py -d 60 --trend 1 --trend-threshold 10
```

- 显示一切日志，并设置所有弹窗持续20秒

```bash
weiboSpider> python .\BoomDetecter.py --log --duration 20
```

## 二次开发

代码写的很简单，二次开发难度也很容易，欢迎随意二次开发。
在weibo.py中还有一些单独操作热搜榜数据的内容，可以玩玩。
