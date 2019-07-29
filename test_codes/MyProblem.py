# -*- coding: utf-8 -*-
"""
作者：李文卓
日期：2019/7/28
功能：对ORS调度的问题进行描述的类class MyProblem
版本：1.0
"""

import numpy as np
import geatpy as ea

class MyProblem(ea.Problem):
    def __init__(self,Num,n_x):
        #n_x表示的是手术室的数量
        #Num表示的是病人的数量
        self.name = 'MyProblem' #初始化函数名
        self.M = 1 #目标维数
        self.maxormins = [1]*self.M #所有目标都被要求最小化
        self.Dim = Num  #决策变量维数，病人的个数
        self.varTypes = np.array([1]*self.Dim)  #初始化varTypes决策变量的类型，离散
        lb = [1]*self.Dim #决策变量下界   #决策变量下界是1
        ub = [n_x]*self.Dim #决策变量上界  #决策变量上界是n_x 手术室数
        self.ranges = np.array([lb,ub]) #初始化ranges(决策变量范围矩阵)   #决策边界
        lbin = [1]*self.Dim #包含决策边界下界
        ubin = [1]*self.Dim #包含决策边界上界
        self.borders = np.array([lbin,ubin])  #初始化borders   #给出被包含的决策边界

    def aimFunc(self,sum_1,sum_2,CV):  #给出目标函数
        f = sum_1+sum_2   #给出目标函数
        return f,CV

    def calBest(self):
        realBestObjV = None
        return realBestObjV




