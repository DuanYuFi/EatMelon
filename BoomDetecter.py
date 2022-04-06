import time
import argparse

from weibo import getHots

from win10toast import ToastNotifier

def getTimeStr(format="%Y-%m-%d %H:%M:%S"):
    return '[%s]' % time.strftime(format, time.localtime())

def getLogHeader(tag, format="%Y-%m-%d %H:%M:%S"):
    return ('[%s]' % tag) + getTimeStr(format)

parser = argparse.ArgumentParser(description='A Weibo hotrank detecter')

parser.add_argument('-d', "--delay", type=int, default=600, help="delay between two checks, seconds")
parser.add_argument("--duration", type=int, default=5, help="Duration of notification")
parser.add_argument('-s', "--slient", action="store_true", help="Show notifications only in shell")
parser.add_argument('-l', "--log", action="store_true", help="Show logs in shell")
parser.add_argument("--show-top", choices=['shell', 'notification', '0', '1'], help="Show the top topic. Shell or 0: show in shell; notification or 1: show in notifications")
parser.add_argument("--trend", choices=['shell', 'notification', '0', '1'], help="Show the fastest increase topic. Shell or 0: show in shell; notification or 1: show in notifications")
parser.add_argument("--trend-threshold", type=int, default=0, help="Threshold of trend analyze")


args = parser.parse_args()

boomToast = ToastNotifier()
topToast = ToastNotifier()
trendToast = ToastNotifier()

print("Service Running...")
last_top_one = None

prev = []
booms = []

while True:
    hots = getHots()
    if hots == False:
        print(getLogHeader("error") + " Banned from server. Wait %d seconds" % args.delay)
        time.sleep(args.delay)
        continue

    newBoom = []
    thisBoom = []
    for each in hots:
        if 'label_name' not in each:
            continue
        if each['label_name'] == '爆':
            thisBoom.append(each['word'])
            if each['word'] not in booms:
                newBoom.append(each['word'])
    
    booms = thisBoom

    if args.log:
        print(getLogHeader("info") + ': ', end='')
        print("Getting new hots.")

    if len(newBoom) != 0:
        msg = '\n'.join(newBoom)
        if args.slient:
            print(getLogHeader("info") + ': ')
            print("新 \"爆\" 热搜:", msg)
        else:
            boomToast.show_toast(title="新 \"爆\" 热搜", msg=msg, duration=args.duration)
            if args.log:
                print(getLogHeader("info") + ': ')
                print("新 \"爆\" 热搜:", msg)
    
    if args.show_top:
        msg = "新热搜榜一: " + hots[1]['word'] + (' [%s]' % hots[1]['label_name']) + ' %d' % hots[1]['num']
        if hots[1]['word'] == last_top_one:
            if args.log:
                print(getLogHeader("info") + ': ', end='')
                print("No new top1.")
            
        else:
            last_top_one = hots[1]['word']

            if args.show_top == '0' or args.show_top == 'shell':
                print(getLogHeader("info") + ': ', end='')
                print(msg)
            else:
                topToast.show_toast(title="新热搜榜一", msg=msg, duration=args.duration)
                if args.log:
                    print(getLogHeader("info") + ': ', end='')
                    print(msg)

    if args.trend:
        best = None
        best_score = args.trend_threshold
        prev_position = 0
        for i, each in enumerate(hots[1:]):
            word = each['word']
            if word in prev:
                prev_position = prev.index(word)
                if prev_position - i > best_score:
                    best_score = prev_position - i
                    best = word
            else:
                continue
        
        if best is not None:
            msg = "上升最快热搜: " + best + ' ' + str(best_score)
            if args.trend == '0' or args.trend == 'shell':
                print(getLogHeader("info") + ': ', end='')
                print(msg)
            else:
                trendToast.show_toast(title="增速最快", msg=msg, duration=args.duration)
                if args.log:
                    print(getLogHeader("info") + ': ', end='')
                    print(msg)
        else:
            if args.log:
                print(getLogHeader("info") + ': ' + "No meaningful increasement.")
        
        prev = [each['word'] for each in hots[1:]]

    time.sleep(args.delay)