# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea

"""
该案例展示了一个离散决策变量的最小化目标的双目标优化问题。
min f1 = -25 * (x1 - 2)**2 - (x2 - 2)**2 - (x3 - 1)**2 - (x4 - 4)**2 - (x5 - 1)**2
min f2 = (x1 - 1)**2 + (x2 - 1)**2 + (x3 - 1)**2 + (x4 - 1)**2 + (x5 - 1)**2
s.t.
x1 + x2 >= 2
x1 + x2 <= 6
x1 - x2 >= -2
x1 - 3*x2 <= 2
4 - (x3 - 3)**2 - x4 >= 0
(x5 - 3)**2 + x4 - 4 >= 0
x1,x2,x3,x4,x5 ∈ {0,1,2,3,4,5,6,7,8,9,10}
"""

class MyProblem(ea.Problem): # 继承Problem父类
    def __init__(self, M = 2):
        self.name = 'MyProblem' # 初始化name（函数名称，可以随意设置）
        self.M = M # 初始化M（目标维数）    目标维数  == 2
        self.maxormins = [1] * self.M # 初始化maxormins（目标最小最大化标记列表）  #所有目标都被要求最小化
        self.Dim = 5 # 初始化Dim（决策变量维数）   决策变量维数  == 5
        self.varTypes = np.array([1] * self.Dim) # 初始化varTypes（决策变量的类型）  #决策变量是离散的
        lb = [0] * self.Dim # 决策变量下界      #  决策变量下界是 0
        ub = [10] * self.Dim # 决策变量上界     #  决策变量上界是 10
        self.ranges = np.array([lb, ub]) # 初始化ranges（决策变量范围矩阵）   # 决策边界
        lbin = [1] * self.Dim    # 是否包含边界，边界被包含
        ubin = [1] * self.Dim
        self.borders = np.array([lbin, ubin]) # 初始化borders（决策变量范围边界矩阵）   给出被包含的边界
    
    def aimFuc(self, Vars, CV):
        x1 = Vars[:, [0]]
        x2 = Vars[:, [1]]
        x3 = Vars[:, [2]]
        x4 = Vars[:, [3]]
        x5 = Vars[:, [4]]   #x1,x2,x3,x4,x5分别是Vars的列向量
        f1 = -25 * (x1 - 2)**2 - (x2 - 2)**2 - (x3 - 1)**2 - (x4 - 4)**2 - (x5 - 1)**2
        f2 = (x1 - 1)**2 + (x2 - 1)**2 + (x3 - 1)**2 + (x4 - 1)**2 + (x5 - 1)**2       #约束函数
        #非操作时间
        #外运转时间

        #患者状态 -- 记录时间
        #单间手术室 -- 记录状态

        #        # 利用罚函数法处理约束条件
#        idx1 = np.where(x1 + x2 < 2)[0]
#        idx2 = np.where(x1 + x2 > 6)[0]
#        idx3 = np.where(x1 - x2 < -2)[0]
#        idx4 = np.where(x1 - 3*x2 > 2)[0]
#        idx5 = np.where(4 - (x3 - 3)**2 - x4 < 0)[0]
#        idx6 = np.where((x5 - 3)**2 + x4 - 4 < 0)[0]
#        exIdx = np.unique(np.hstack([idx1, idx2, idx3, idx4, idx5, idx6])) # 得到非可行解的下标
#        f1[exIdx] = f1[exIdx] + np.max(f1) - np.min(f1)
#        f2[exIdx] = f2[exIdx] + np.max(f2) - np.min(f2)
        # 利用可行性法则处理约束条件
        CV = np.hstack([2 - x1 - x2,
                        x1 + x2 - 6,
                        -2 - x1 + x2,
                        x1 - 3*x2 - 2,
                        (x3 - 3)**2 + x4 - 4,
                        4 - (x5 - 3)**2 - x4])    #约束函数
        return np.hstack([f1, f2]), CV
        # ObjV表示种群的目标函数值矩阵，每行对应一个个体，每列对应一个目标
        # CV用于定量描述违反约束条件的矩阵，每行对应一个个体，每列对应一个约束
    
    def calBest(self):
        realBestObjV = None
        return realBestObjV

    #用于计算全局最优解    realBestObjV存的是实际最佳的目标函数数值矩阵