#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------
# @Author: dwqq
# @Date  : 2020/10/30 15:09 
# @File  : tecplot_run.py
# @IDE   : PyCharm
# -------------------------------
import os
from string import Template


def generate_mcr(old_mcr, new_mcr, op2_file, order_num, save_path):
    """利用Template生成新的tecplot宏文件
    old_mcr为模板
    new_mcr为需要创建的文件"""
    mcr_tmp = open(old_mcr, 'r')
    mcr_gen = open(new_mcr, 'w')
    line = mcr_tmp.readline()
    while line:
        if '${op2_file}' in line and '${order_num}' in line:
            line_list = line.split("'")
            line_tmp = Template(line_list[1])
            line_1 = line_tmp.substitute(op2_file=op2_file, order_num=order_num)
            line = line_list[0] + "'" + line_1 + "'\n"
        elif '${save_path}' in line and '${order_num}' in line:
            line_list = line.split("'")
            line_tmp = Template(line_list[1])
            line_1 = line_tmp.substitute(save_path=save_path, order_num=order_num)
            line = line_list[0] + "'" + line_1 + "'\n"
        mcr_gen.write(line)
        line = mcr_tmp.readline()
    mcr_tmp.close()
    mcr_gen.close()


def call_tecplot(tecplot_dir, mcr_file):
    """利用tecplot进行nastran结果后处理，生成云图
    -b 代表的批处理模式，加上此选项后不会启动tecplot的GUI
    -p 表示tecplot后面跟的是一个宏文件"""
    # 切换到tecplot安装目录下执行
    os.chdir(tecplot_dir)
    os.system('tec360.exe -b -p ' + mcr_file)


def main(n_order):
    """nastran模态分析结果，利用tecplot进行后处理，得到前8阶振型云图"""
    tecplot_dir = 'F:\\software_install\\Tecplot\\Tecplot 360 EX 2018 R1\\bin'
    cur_dir = os.getcwd()
    mcr_template = os.path.join(cur_dir, 'tec_nast_template.mcr')
    op2_f = os.path.join(cur_dir, 'nastran_result.op2')
    save_exc = cur_dir
    for order in range(1, n_order+1):
        # # op2文件中第3阶、第6阶、第8阶为面内位移
        # if order < 3:
        #     order_id = order
        # elif 3 < order < 8:
        #     order_id = order - 1
        # elif order > 8:
        #     order_id = order - 2
        # else:
        #     continue

        # 生成tecplot宏文件mcr
        mcr_gen_name = 'tec_nast_' + str(order) + '.mcr'
        mcr_gen_f = os.path.join(os.getcwd(), mcr_gen_name)
        print(mcr_gen_f)
        generate_mcr(mcr_template, mcr_gen_f, op2_f, order, save_exc)

        # 执行tecplot
        call_tecplot(tecplot_dir, mcr_gen_f)
        os.chdir(cur_dir)


if __name__ == '__main__':
    main(10)

