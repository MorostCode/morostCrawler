# -*- coding: utf-8 -*- 
# @Time: 2024/6/8 上午1:24 
# @Author: morost
# @File: commonFunction.py 
# @desc:

# 格式化字符串
def strFormat(str_in):
    str_out = str_in.strip().replace('\n', '').replace('\t', '').replace('\xa0', ' ')
    return str_out


if __name__ == '__main__':
    pass
