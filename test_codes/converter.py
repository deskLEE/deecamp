"""
作者：lwz
日期：2019/7/29
功能：生成测试代码
版本：v1.0
"""

import xlrd
import json
wb = xlrd.open_workbook('input.xlsx')
sheet1 = wb.sheet_by_index(0)
n_p = sheet1.nrows
n_l = sheet1.ncols

rows = sheet1.row_values(0)  # 获取第1行内容 list
input = []
for i in range(1,n_p):
    input.append(dict(zip(rows,sheet1.row_values(i))))
input.sort(key = lambda input: input['就诊号'])

f = open('input.json', 'w', encoding='utf-8')
json.dump(input, f, ensure_ascii=False,indent=4)
f.close()

