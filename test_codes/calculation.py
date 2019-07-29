"""
作者：desklee
日期：2019/7/29
功能：计算对象
"""
import json
class calculte():
    def __init__(self,input_1,n_x,n_y,t_s,morning_time,afternoon_time):
        self.input_1 = input_1
        self.n_x = n_x
        self.n_y = n_y
        self.t_s = t_s
        self.morning = morning_time
        self.afternoon_time = afternoon_time

    def _process_date_(self,num):
        list_doctID = []          #doctID是医生号
        list_sleepy = []          #是否复苏
        list_operation = []       #手术时间
        list_clean = []           #清洁时间
        i = 1
        for pk in range(num):
            self.input_1[pk]['序号'] = i
            i += 1
            list_doctID.append(self.input_1[pk]['序号'])
            list_sleepy.append(self.input_1[pk]['麻醉方式'])
            list_operation.append(self.input_1[pk]['手术时长(分钟)'])
            a = self.input_1[pk]['手术级别']
            if a == '1.0':
                tp = 10
            elif a == '2.0' or a == '3.0':
                tp = 20
            else:
                tp = 30
            list_clean.append(tp)

        return list_doctID,list_sleepy,list_operation,list_clean

    def _output_date_(self):
        f = open('output.json', 'w', encoding='utf-8')
        json.dump(self.input_1, f, ensure_ascii=False, indent=4)
        f.close()



#  def output(self,):
 #       return
