#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------
# @Author: dwqq
# @Date  : 2020/10/23 14:34 
# @File  : patran_run.py
# @IDE   : PyCharm
# -------------------------------
import os


def create_patran_ses(ses_template, new_ses, new_path):
    """利用ses模板创建新的ses文件"""
    old_f = open(ses_template, 'r')
    new_f = open(new_ses, 'w')
    old_path = 'E:\\work\\nastran_patran\\code\\test1'
    for line in old_f.readlines():
        if old_path in line:
            line = line.replace(old_path, new_path)
        new_f.write(line)
    old_f.close()
    new_f.close()


def run(patran_path, ses_file):
    """运行patran"""
    os.system(patran_path + ' -sfp ' + ses_file)


if __name__ == '__main__':
    # 获取上一级目录
    # parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))

    # old_file = os.path.join(os.getcwd(), 'test.ses.01')
    # new_file = os.path.join(os.getcwd(), 'test1.ses.01')
    # print(new_file)
    # save_path = os.path.join(os.getcwd(), 'test2')

    # create_patran_ses(old_file, new_file, save_path)

    new_file = os.path.join(os.getcwd(), 'test_dwqq.ses.01')
    patran_exe = "F:\\MSC.Software\\Patran_x64\\20121\\bin\\patran.exe"
    run(patran_exe, new_file)


    

