# -*- coding: utf-8 -*-
import geatpy as ea # import geatpy
from MyProblem import MyProblem # 导入自定义问题接口

"""==================================实例化问题对象================================"""
problem = MyProblem() # 生成问题对象，实例化MyProblem的对象

"""==================================种群设置================================"""
Encoding = 'I'             # 编码方式  ，这种编码方式是整数
conordis = 1               # 表示染色体解码后得到的变量是离散的   表示解码后的变量是离散的//1表示的是连续
NIND = 50                  # 种群规模，总变量个数是50，解空间个数是50
Field = ea.crtfld(Encoding, conordis, problem.ranges, problem.borders) # 创建区域描述器   根据编码方式/解码后的变量类型/决策边界/
## 包含边界来确定区域描述
population = ea.Population(Encoding, conordis, Field, NIND) # 实例化种群对象（此时种群还没被真正初始化）
#用编码方式/解码后的变量类型/解空间/种群规模来初始化population
"""==================================算法参数设置================================"""
myAlgorithm = ea.moea_NSGA2_templet(problem, population) # 实例化一个算法模板对象,传入problem/population，
# 也就是生成问题对象和种群对象
myAlgorithm.MAXGEN = 200 # 最大遗传代数
"""=======================调用算法模板进行种群进化=============================="""
NDSet = myAlgorithm.run() # 执行算法模板，得到帕累托最优解集NDSet，直接输出解集
print(population.FitnV)
# 输出
#print('用时：%s 秒'%(myAlgorithm.passTime))
#print('非支配个体数：%s 个'%(NDSet.sizes))
#print(NDSet.Phen.shape)
#print(NDSet.Phen)
#patore
#print('单位时间找到帕累托前沿点个数：%s 个'%(int(NDSet.sizes // myAlgorithm.passTime)))
