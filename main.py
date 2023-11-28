# -*-coding:utf-8-*-
# cython:language_level=3
import sys
import MyMka
import numpy as np
#import matplotlib.pyplot as plt

def main(file):
    #0.初始化参数获取
    if file=="":file=myGUI.getFile("csv")
    if file=="":return
    #1.读取mka文件
    bsc,ms,eA,eB,pl,pr,ll,lr=MyMka.getCSV(file)
    #2.数据堆叠处理

    #3.数据搭接处理

    #4.分度误差处理


    #5.结果现实