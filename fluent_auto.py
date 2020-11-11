#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------
# @Author: dwqq
# @Date  : 2020/11/10 9:55 
# @File  : sim_auto.py
# @IDE   : PyCharm
# -------------------------------
import os
import shutil
from string import Template
import math
import numpy as np
import logger
import traceback
import pandas as pd
from multiprocessing import Process


class FluentSim(object):
    """fluent仿真自动化"""
    def __init__(self, input_file=None, temp_file=None, exec_path=None, result_dir=None, data_merge=None,
                 iter_num=200, epoch_num=5, ma_min=0, ma_max=0.8, aoa_min=0, aoa_max=6):
        """
        :param input_file: 仿真应用的输入文件
        :param temp_file: 仿真脚本模板
        :param exec_path: 应用安装或执行路径
        :param result_dir: 结果存放目录
        :param iter_num: 迭代次数
        :param epoch_num: 循环次数
        :param ma_min: 最小马赫数
        :param ma_max: 最大马赫数
        :param aoa_min: 最小攻角
        :param aoa_max: 最大攻角
        :param data_merge: 结果数据收集文件
        """
        self.input_file = input_file
        self.temp_file = temp_file
        self.exec_path = exec_path
        self.result_dir = result_dir
        self.iter_num = iter_num
        self.epoch_num = epoch_num
        self.ma = np.random.permutation(np.linspace(ma_min, ma_max, self.epoch_num))    # 随机排列
        self.aoa = np.random.permutation(np.linspace(aoa_min, aoa_max, self.epoch_num))
        self.data_merge = data_merge

        # 创建结果目录
        if os.path.exists(self.result_dir):
            shutil.rmtree(self.result_dir)
        if not os.path.exists(self.result_dir):
            os.mkdir(self.result_dir)

    def generate_fluent_script(self, scr_file=None, save_dir=None, new_ma=0.6, new_aoa=2):
        """
        利用fluent脚本模板创建新的脚本
        :param scr_file: fluent脚本文件
        :param save_dir: 结果保存目录
        :param new_ma: 马赫数
        :param new_aoa: 攻角
        :return:
        """
        temp_f = open(self.temp_file, 'r')
        scr_f = open(scr_file, 'w')
        line = temp_f.readline()
        while line:
            if '${RESULT_DIR}' in line and '${COS_AOA}' not in line:
                line_temp = Template(line)
                line = line_temp.substitute(RESULT_DIR=save_dir)
            elif '${INPUT_FILE}' in line:
                line_temp = Template(line)
                line = line_temp.substitute(INPUT_FILE=self.input_file)
            elif '${COS_AOA}' in line and '${SIN_AOA}' in line:
                cos_aoa = math.cos(math.radians(new_aoa))   # 将角度转为弧度计算cos
                sin_aoa = math.sin(math.radians(new_aoa))
                line_temp = Template(line)
                if '${MA}' in line:
                    line = line_temp.substitute(MA=new_ma, COS_AOA=cos_aoa, SIN_AOA=sin_aoa)
                else:
                    line = line_temp.substitute(RESULT_DIR=save_dir, COS_AOA=cos_aoa, SIN_AOA=sin_aoa)
            elif '${ITER_NUM}' in line:
                line_temp = Template(line)
                line = line_temp.substitute(ITER_NUM=self.iter_num)
            scr_f.write(line)
            line = temp_f.readline()
        temp_f.close()
        scr_f.close()

    def call_fluent(self, scr_file=None):
        """
        启动fluent
        :param scr_file: 新创建的fluent脚本文件
        :return:
        """
        os.system(self.exec_path + ' 2ddp -t0 -i' + scr_file)    # -g不启动图像界面

    @staticmethod
    def get_last_line(file_name):
        """读取结果文件的最后一行"""
        try:
            file_size = os.path.getsize(file_name)
            # print('file_size: ', file_size)
            if file_size == 0:
                return None
            else:
                with open(file_name, 'rb') as fp:
                    offset = -20
                    while -offset < file_size:
                        fp.seek(offset, 2)      # 从文本末尾开始，定位到offset的位置
                        lines = fp.readlines()  # 读取offset之后的所有文本
                        if len(lines) >= 2:
                            return lines[-1]
                        else:
                            offset *= 2
                    fp.seek(0)
                    lines = fp.readlines()
                    return lines[-1]
        except FileNotFoundError:
            print(file_name + 'not found')
            return None

    def data_collection(self, sim_dir, data_file_name):
        """结果数据收集"""
        data_dic = {}
        for file in os.listdir(sim_dir):
            if file.split('.')[-1] == 'out':
                data_binary = self.get_last_line(os.path.join(sim_dir, file))
                data_str = data_binary.decode(encoding='utf-8').strip(' \r\n')
                data = data_str.split(' ')[-1]
                if 'cl' in file:
                    data_dic['cl'] = data
                elif 'cd' in file:
                    data_dic['cd'] = data
                elif 'cm' in file:
                    data_dic['cm'] = data
        print(data_dic)
        data_pd = pd.DataFrame(data_dic, index=[0], columns=['cl', 'cd', 'cm'])
        data_pd.to_csv(data_file_name, index=None, mode='a', header=False)

    def fluent_main(self):
        """
        批量执行fluent
        :return:
        """
        for i in range(self.epoch_num):
            log.logger.info('第{}次循环' .format(i+1))
            sim_subdir = os.path.join(self.result_dir, 'fluent_sim_' + str(i))
            os.mkdir(sim_subdir)
            scr_file = os.path.join(sim_subdir, 'fluent_scr.jou')
            log.logger.info('仿真参数：Ma--{0}, AOA--{1}' .format(self.ma[i], self.aoa[i]))
            log.logger.info('创建仿真脚本')
            try:
                self.generate_fluent_script(scr_file=scr_file, save_dir=sim_subdir,
                                            new_ma=self.ma[i], new_aoa=self.aoa[i])
            except Exception as err:
                log.logger.info('仿真脚本创建失败：' + repr(err))
                log.logger.debug(traceback.format_exc())
            log.logger.info('执行仿真')
            try:
                self.call_fluent(scr_file=scr_file)
            except Exception as err:
                log.logger.info('仿真运行失败：' + repr(err))
                log.logger.debug(traceback.format_exc())
            if self.data_merge is not None:
                log.logger.info('结果收集')
                data_merge_file = os.path.join(result_dir, self.data_merge + '.csv')
                try:
                    self.data_collection(sim_subdir, data_merge_file)
                except Exception as err:
                    log.logger.info('结果收集失败：' + repr(err))
                    log.logger.debug(traceback.format_exc())


if __name__ == '__main__':
    log_file = os.path.join(os.getcwd(), 'log.txt')
    log = logger.Logger(log_file, level='debug')
    input_file = os.path.join(os.getcwd(), 'fluent/AIRFOIL.MSH')
    temp_file = os.path.join(os.getcwd(), 'fluent/journal_template.jou')
    exec_path = 'F:/software_install/"ANSYS Inc"/v192/fluent/ntbin/win64/fluent.exe'    # windows
    # exec_path = '/public/software/ansys_inc/v192/fluent/bin/fluent'    # linux
    result_dir = os.path.join(os.getcwd(), 'fluent/result')
    data_merge_name = 'data_merge'
    fluent_sim = FluentSim(input_file=input_file, temp_file=temp_file, exec_path=exec_path, result_dir=result_dir,
                           data_merge=data_merge_name, iter_num=200, epoch_num=5, ma_min=0, ma_max=0.8,
                           aoa_min=0, aoa_max=6)
    fluent_sim.fluent_main()

