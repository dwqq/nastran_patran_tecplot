#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------
# @Author: dwqq
# @Date  : 2020/10/30 15:09 
# @File  : tecplot_run.py
# @IDE   : PyCharm
# -------------------------------
import os


def call_tecplot(tecplot_dir, mcr_file):
    """利用tecplot进行nastran结果后处理，生成云图
    -b 代表的批处理模式，加上此选项后不会启动tecplot的GUI
    -p 表示tecplot后面跟的是一个宏文件"""
    os.chdir(tecplot_dir)
    os.system('tec360.exe -b -p ' + mcr_file)


if __name__ == '__main__':
    tecplot_dir = 'F:\\software_install\\Tecplot\\Tecplot 360 EX 2018 R1\\bin'
    mcr_f = os.path.join(os.getcwd(), 'tecplot_nastran.mcr')
    call_tecplot(tecplot_dir, mcr_f)
