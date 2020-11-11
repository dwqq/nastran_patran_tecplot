#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------
# @Author: dwqq
# @Date  : 2020/10/29 14:35 
# @File  : nastran_run.py
# @IDE   : PyCharm
# -------------------------------

import os
import math
import random
import shutil


def generate_new_bdf(old_bdf, new_bdf, new_thickness=None, new_E=None, new_density=None):
    """修改原bdf文件，生成新的bdf文件修改参数：PSHELL厚度，材料属性MAT1弹性模量和密度"""
    old_f = open(old_bdf, 'r')
    new_f = open(new_bdf, 'w')
    for line in old_f.readlines():
        if 'PSHELL' in line and new_thickness is not None:
            old_thickness = get_old_param(line, 3)
            line = line.replace(old_thickness, new_thickness)
        if 'MAT1' in line:
            old_E = get_old_param(line, 2)
            old_density = get_old_param(line, 5)
            if new_E is not None:
                line = line.replace(old_E, new_E)
            if new_density is not None:
                line = line.replace(old_density, new_density)
        new_f.write(line)
    old_f.close()
    new_f.close()


def get_old_param(string, index):
    """从字符串中提取指定位置的参数"""
    param_list = []
    str_len = len(string)
    param_num = math.ceil(str_len/8)
    for i in range(param_num):
        param = string[8*i:8*(i+1)].strip()
        param_list.append(param)
    out_param = param_list[index]
    return out_param


def call_nastran(nastran_exec, bdf_file):
    os.system(nastran_exec + ' ' + bdf_file + ' scr=yes')
    # os.system(nastran_exec + ' ' + bdf_file)


def dir_opt(dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


def result_collection(res_file, merge_file):
    """收集结果文件"""
    res_f = open(res_file, 'r')
    merge_f = open(merge_file, 'a')
    line = res_f.readline()
    while line:
        if 'E I G E N V A L U E S' in line:
            for _ in range(12):
                line = res_f.readline()
                merge_f.writelines(line)
                # print(line, end='')
        else:
            line = res_f.readline()
    merge_f.writelines('\n')
    res_f.close()
    merge_f.close()


def main(n):
    nastran_exe = 'F:\\MSC.Software\\MSC_Nastran\\20121\\bin\\nastran'
    # bdf_dir = os.path.join(os.getcwd(), 'nastran_bdf_test')
    bdf_dir = os.getcwd()
    old_bdf = os.path.join(bdf_dir, 'nastran_bdf.bdf')
    merge_file = os.path.join(bdf_dir, 'result_merge.dat')
    if os.path.exists(merge_file):
        os.remove(merge_file)

    # 新参数列表
    thickness_list = ['1.', '2.', '3.', '4.']
    elastic_list = ['2.1+11', '1.7+11', '3.5+11', '5.1+11']
    density_list = ['7650.', '8500.', '5600.', '9800.']

    for i in range(n):
        print('第%d次运行' % (i+1))
        # 创建新的文件夹和新bdf文件
        dir_name = 'nastran_test_' + str(i)
        new_dir = os.path.join(bdf_dir, dir_name)
        dir_opt(new_dir)
        new_bdf = os.path.join(new_dir, 'test.bdf')
        print('bdf路径：' + new_bdf)
        # 新参数
        random_list = random.sample([i for i in range(len(thickness_list))], 3)
        new_thick = thickness_list[random_list[0]]
        new_elast = elastic_list[random_list[1]]
        new_dens = density_list[random_list[2]]
        print('新参数：new_thick--%s, new_elast--%s, new_dens--%s' % (new_thick, new_elast, new_dens))

        # 写入新参数到结果收集文件
        with open(merge_file, 'a') as mer_f:
            mer_f.writelines('{0:<15}{1:>10}\n{2:<15}{3:>10}\n{4:<15}{5:>10}\n'
                             .format('Thickness:', new_thick, 'Elastic_module:', new_elast, 'Density:', new_dens))

        generate_new_bdf(old_bdf, new_bdf, new_thickness=new_thick, new_E=new_elast, new_density=new_dens)
        print('新bdf文件创建成功')
        call_nastran(nastran_exe, new_bdf)

        # 移动结果文件
        for file_name in os.listdir(os.getcwd()):
            if file_name.split('.')[-1] in ['f04', 'f06', 'log', 'op2']:
                shutil.move(os.path.join(os.getcwd(), file_name), new_dir)

        # 收集结果
        for file_name in os.listdir(new_dir):
            if file_name.split('.')[-1] == 'f06':
                result_file = os.path.join(new_dir, file_name)
                result_collection(result_file, merge_file)


if __name__ == '__main__':
    main(4)

    # result_file = os.path.join(os.getcwd(), 'nastran_bdf_test/nastran_test_0/test.f06')
    # merge_file = os.path.join(os.getcwd(), 'nastran_bdf_test/result_merge.dat')
    # result_collection(result_file, merge_file)
