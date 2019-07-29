"""
作者：李文卓
日期：2019/7/29
用途：主程序
"""
import json
from calculation import calculte
from MyProblem import MyProblem
import geatpy as ea
from algorithm import Algorithm

def _get_json_(filepath):
    with open(filepath,mode='r',encoding='utf-8') as f:
        number = json.load(f)
    return number


def main():
    filepath_1 = 'input.json'
    input_1 = _get_json_(filepath_1)
    num = len(input_1)  # 总的数目
#    filepath_1 = 'result.json'
#    city_list = _get_json_(filepath_1)
#    print(type(city_list))
    filepath_2 = 'num.json'
    number = _get_json_(filepath_2)
    for fi in number:
        n_x = int(fi['n_x'])    #手术室数目
        n_y = int(fi['n_y'])    #复苏室数目
        t_s = int(fi['t_s'])    #最短复苏时间
        morning_time = int(fi['morning_time'])    #上班时间
        afternoon_time = int(fi['afternoon_time'])#下班时间

    calculte_r = calculte(input_1,n_x,n_y,t_s,morning_time,afternoon_time)  # 实例化
    list_doctID, list_sleepy, list_operation, list_clean = calculte_r._process_date_(num)

    Encoding = 'I'  # 编码方式为实数
    conordis = 0  # 染色体解码后得到的变量是连续的
    NIND = 40  # 种群规模

    problem = MyProblem(num, n_x)  # 生成问题对象
    Field = ea.crtfld(Encoding, conordis, problem.ranges, problem.borders)  # 创建区域描述器
    population = ea.Population(Encoding, conordis, Field, NIND)         # 创建种群对象



    calculte_r._output_date_()  #返回输出




#运行主程序
if __name__ == '__main__':
    main()