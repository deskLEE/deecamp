# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 09:55:36 2019

@author: 74711
"""

"""模拟手术室整个工作流程，每5分钟检查一次，得到最终优化目标结果"""
import numpy as np

n_o = 3
n_r = 2
chrom = np.array([1,2,3,2,1,3])
o_time = np.array([60,40,35,30,45,50])
c_time = np.array([20,20,20,20,20,20])
r_time = np.array([60,60,60,60,60,60])


def simulation(n_o, n_r, chrom, o_time, c_time, r_time):
    # n_o为手术室数量，n_r为复苏室数量, chrom为染色体[1,3,2]表示第一台
    # 手术在1号手术室在1号手术室内做，o_time[30,100,60]表示第一台手术时长30分钟，
    # c_time表示清洁时长，r_time表示复苏时长（0或自定义最小复苏时长默认为60min）
    r_time_max = r_time.max()  # 最小复苏时长
    o_o_state = np.zeros(n_o, dtype=np.bool)  # 手术室是否进行手术
    o_c_state = np.zeros(n_o, dtype=np.bool)  # 手术室是否进行清洁
    o_r_state = np.zeros(n_o, dtype=np.bool)  # 手术室是否进行复苏
    o_end_state = np.zeros(n_o, dtype=np.bool)  # 手术室是否结束工作
    r_state = np.zeros(n_r, dtype=int)  # 复苏室内状态，0表示空置，大于0表示在使用
    r_empty_num = n_r  # 有几个复苏室空床位
    o_total_time = np.zeros(n_o, dtype=int)  # 各手术室内工作总时长（直到最后一台手术完成清洁）
    o_total_r_time = np.zeros(n_o, dtype=int)  # 各手术室内复苏总时长
    o_total_empty_time = np.zeros(n_o, dtype=int)  # 各手术室内日常工作时段的闲置总时长（既不做手术，也不清洁，不复苏）
    overtime_work = np.zeros(n_o, dtype=int)
    o_dict = {}  # 一个存放每个手术室室染色体上第几台手术的字典，如{1：[2,4,5]表示第一号手术室按顺序做染色体上第2，4，5台手术
    o_order = np.zeros(n_o, dtype=int)  # 存放目前该手术室正在进行第几台手术
    o_len = np.zeros(n_o, dtype=int)  # 存放每个手术室有几台手术
    o_o_time = np.zeros(n_o, dtype=int)  # 目前手术室内手术还需要多长时间
    o_c_time = np.zeros(n_o, dtype=int)  # 目前手术室内清洁还需要多长时间
    o_r_time = np.zeros(n_o, dtype=int)  # 目前手术室内已复苏了多长时间
    work_time = (16 - 8) * 60 / 5  # 日常工作时长有多少个5分钟
    for o in range(n_o):
        o_dict[o] = np.where(chrom == o + 1)[0]
        o_len[o] = o_dict[o].shape[0]

    for t in range(288):
        # 一天排班最多24小时，每5分钟检查一次
        r_empty_num = r_state[r_state == 0].size  # 空复苏室床位个数
        if o_r_state[o_r_state == True].size > 0 and r_empty_num > 0:
            o_r_time_sort = np.argsort(-o_r_time)
            for r in range(r_empty_num):
                o_room = o_r_time_sort[r]
                if o_r_time[o_room] == 0:
                    break
                o_r_state[o_room] = False
                o_total_r_time += o_r_time[o_room]
                o_total_time += o_r_time[o_room]
                o_c_state[o_room] = True
                o_c_time[o_room] = c_time[o_dict[o][o_order[o]]]
                r_empty_num -= 1

        r_state[r_state > 0] -= 5  # 更新复苏室床位状态
        for o in range(n_o):
            # 对每个手术室状态进行检查
            if o_end_state.sum() == n_o:
                break
            if o_end_state[o] == True:  # 如果已结束当天所有工作，进入下一个手术室循环
                continue

            if o_o_state[o] == False and o_c_state[o] == False and o_r_state[o] == False:
                o_o_state[o] = True
                o_o_time[o] = o_time[o_dict[o][o_order[o]]] - 5  # 将第i台的手术时长填入减5
                if o_o_time[o] == 0:
                    o_total_time[o] += o_time[o_dict[o][o_order[o]]]  # 将这一台手术时长计入工作总时间
                    if r_time[o_dict[o][o_order[o]]] == 0:
                        o_c_state[o] = True
                        o_c_time[o] = c_time[o_dict[o][o_order[o]]]
                    else:
                        if r_empty_num == 0:
                            o_r_state[o] = True
                        else:
                            r_state[np.where(r_state == 0)[0]] += r_time_max
                            r_empty_num -= 1

            elif o_o_state[o] == True:
                o_o_time[o] -= 5
                if o_o_time[o] == 0:
                    o_total_time[o] += o_time[o_dict[o][o_order[o]]]  # 将这一台手术时长计入工作总时间
                    if r_time[o_dict[o][o_order[o]]] == 0:
                        o_c_state[o] = True
                        o_c_time[o] = c_time[o_dict[o][o_order[o]]]
                    else:
                        if r_empty_num == 0:
                            o_r_state[o] = True
                        else:
                            r_state[np.where(r_state == 0)[0]] += r_time_max
                            r_empty_num -= 1

            elif o_c_state[o] == True:
                o_c_time[o] -= 5
                if o_c_time[o] == 0:
                    o_total_time[o] += c_time[o_dict[o][o_order[o]]]  # 将这一台手术清洁时间计入手术室工作总时间
                    o_order[o] += 1
                    if o_order[o] < o_len[o]:  # 推入下一台手术
                        o_o_state[o] = True
                        o_o_time[o] = o_time[o_dict[o][o_order[o]]]
                    else:
                        o_end_state = True  # 手术室工作结束
                        if t + 1 < work_time:  # 将闲置时间累加
                            o_total_empty_time[o] += (work_time - t - 1) * 5
                        else:
                            overtime_work[o] += (t - work_time + 1) * 5

            elif o_r_state[o] == True:
                o_r_time += 5
                if o_r_time == r_time_max:
                    o_total_r_time += r_time_max
                    o_total_time += r_time_max
                    o_c_state[o] = True
                    o_c_time[o] = c_time[o_dict[o][o_order[o]]]
    return o_total_time.sum(), o_total_r_time.sum(), o_total_empty_time.sum(), overtime_work.sum()


total_time, total_r_time, total_empty_time, overtime = simulation(n_o, n_r, chrom, o_time, c_time, r_time)
f_min = total_r_time + total_empty_time + overtime
print(total_time)
print(total_r_time)
print(total_empty_time)
print(overtime)