# encoding: utf-8
from Simulation import simulation
import numpy as np
num_test=open('num_tests.txt','r')
number=num_test.read()
for text_index in range(1,int(number)+1):
    mode=open('mode_{}.txt'.format(text_index),'r').read()
    if mode=='trace':
        arrival = open('arrival_{}.txt'.format(text_index), 'r').read()
        service = open('service_{}.txt'.format(text_index), 'r').read()
        para = open('para_{}.txt'.format(text_index), 'r').read()
        para_list = para.split('\n')
        arrival_list=np.matrix(arrival)
        arrival_list=arrival_list.tolist()
        arrival_list=arrival_list[0]
        service_list = np.matrix(service)
        service_list=service_list.tolist()
        service_list=service_list[0]
        # print(mode,arrival_list,service_list,para_list[0],para_list[1],para_list[2])
        result=simulation(mode,arrival_list,service_list,int(para_list[0]),float(para_list[1]),float(para_list[2]),float('inf'))
        # print(result[0])
        # print(result[1])
        # print(len(result[1]))
        with open('mrt_{}.txt'.format(text_index),'w') as f:
            f.write("%.3f"%result[0])
        with open('departure_{}.txt'.format(text_index),'w') as f:
            for i in range(len(result[1])):
                for j in range(2):
                    f.write(format(result[1][i][j],'0.3f'))
                    if j ==0:
                        f.write('\t ')
                f.write('\n')
    if mode =='random':
        arrival=open('arrival_{}.txt'.format(text_index),'r').read()
        service=open('service_{}.txt'.format(text_index),'r').read()
        para = open('para_{}.txt'.format(text_index), 'r').read()
        para_list = para.split('\n')
        result=simulation(mode=mode,arrival=float(arrival),service=float(service),m=int(para_list[0]),setup_time=float(para_list[1]),delayedoff_time=float(para_list[2]),end_time=float(para_list[3]))
        with open('mrt_{}.txt'.format(text_index),'w') as f:
            f.write("%.3f"%result[0])
        with open('departure_{}.txt'.format(text_index),'w') as f:
            for i in range(len(result[1])):
                for j in range(2):
                    f.write(format(result[1][i][j],'0.3f'))
                    if j ==0:
                        f.write('\t ')
                f.write('\n')
