#!/usr/bin/python3

'''
FI.py
基礎統制libのFIスクリプト

デフォルトはFI10s, ITI10s, 10試行
'''

__author__ = "Qukoyk"
__contacts__ = "m172236@hiroshima-u.ac.jp"


# 前置き宣言
x = 10  # FI x s
iti = 10  # ITI 10s
trialsMax = 10  # 総回数

# ポート宣言
leverLeftAct = 26
leverLeftMove = 19
leverRightAct = 20
leverRightMove = 16
lightLeft = 6
lightRight = 12
houseLight = 13
feeder = 21
buzzer = 5
handShaping = 25

# import文
import RPi.GPIO as GPIO
from time import sleep
import time
import csv

# ポート設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(feeder, GPIO.OUT)
GPIO.setup(leverLeftMove, GPIO.OUT)
GPIO.setup(leverRightMove, GPIO.OUT)
GPIO.setup(lightLeft, GPIO.OUT)
GPIO.setup(lightRight, GPIO.OUT)
GPIO.setup(houseLight, GPIO.OUT)
GPIO.setup(leverLeftAct, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(leverRightAct, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(handShaping, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 実験開始プロセス
answer2 = input("今回の番号は？:\n")
print("始めますか？")
answer = input("Press y:\n")
while True:
    if answer == "y":
        print("")
        print("=======START!=======")
        print("")
        break
    else:
        sleep(0.1)

# データ初期化
trial = 0
timeCount = 0
time0 = time.time()
time2 = time.time()
timePast = 0
day = time.strftime("%Y-%m-%d")

timeFoolishWayStart = time.time()
timeFoolishWayNow = time.time()
with open(day + "_" + answer2 + '.csv', 'a+') as myfile:
    writer = csv.writer(myfile)
    writer.writerow(['Trial', 'Time'])

# データ保存先を指定
leverLeftActData = []


# メインプログラム
while trial < trialsMax:

    GPIO.output(leverLeftMove, GPIO.HIGH)
    for timeCount in range(x):
        print(timeCount + 1, "s/", x, "s")
        sleep(1)
    while GPIO.input(leverLeftAct) == GPIO.LOW:
        sleep(0.01)

    if GPIO.input(leverLeftAct) == GPIO.HIGH:
        GPIO.output(leverLeftMove, GPIO.LOW)
        GPIO.output(feeder, GPIO.HIGH)
        time1 = time.time()
        trial = trial + 1
        timePast = round(time1 - time0, 2)
        print("Trial ", trial, "/", trialsMax)
        print("Time ", timePast, "\n")
        time2 = time.time()
        leverLeftActData = [str(trial), str(timePast)]
        with open(day + "_" + answer2 + '.csv', 'a+') as myfile:
            writer = csv.writer(myfile)
            writer.writerow(leverLeftActData)
        print("ITI", iti, "s\n")
        sleep(iti)
        time0 = time.time()
        while GPIO.input(leverLeftAct) == GPIO.HIGH:
            sleep(0.01)

    else:
        GPIO.output(feeder, GPIO.LOW)
    sleep(0.01)

else:
    myfile.close()


# ポート釈放
myfile.close()
GPIO.cleanup()
