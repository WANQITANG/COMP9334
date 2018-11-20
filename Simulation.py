# encoding: utf-8
import random
import math
import numpy as np
import matplotlib.pyplot as pl


# def simulation(mode:str,arrival,service,m:int,setup_time:float,delayedoff_time:float,end_time:float):
def simulation(mode, arrival, service, m, setup_time, delayedoff_time, end_time):

    dispatcher=[]
    master_clock = 0
    response_time_cumulative = 0
    num_customer_served = 0
#-------------------------------------------------------------------------------------------------------
    #找出随机的到达时间，和service_time
    AA=[]
    marked=[]
    unmarked=[]
    next_departure_time = float('inf') * np.ones([m, 1])
    next_setup_time=float('inf') * np.ones([m, 1])
    next_delayedoff_time = float('inf')*np.ones([m, 1])
    servers_offs=np.ones([m,1])
#set a array of off 1 means OFF
    servers_busy=float('inf')*np.ones([m,2])##initial 'inf'
    index=0
    random.seed(1)
    if mode=='trace':
        arrival_time_list=arrival
        service_time_list=service
    if mode=='random':
        next_arrival_time = -math.log(1 - random.random()) / arrival
        # ARR.append(next_arrival_time)
        k1=-math.log(1 - random.random()) / service
        k2=-math.log(1 - random.random()) / service
        k3=-math.log(1 - random.random()) / service
        next_service_time =  k1+k2+k3

        ##get a matrix named next_arrival_event including(arrival_time,service_time)
##====================================================================================
    response_time_cumulative_list=[]
    while (master_clock<end_time):
    # while index<=len(arrival_time_list)-1:
    #     print('----------------------------------')
        if mode=='trace':
            if index>len(arrival_time_list)-1:
                next_arrival_time=float('inf')
                next_service_time=float('inf')
            else:
                next_service_time = service_time_list[index]
                # print('下一次到达时间',next_arrival_time)
                next_arrival_time = arrival_time_list[index]
        first_departure_time=min(next_departure_time[:,0])
        first_setup_time_finished=min(next_setup_time[:,0])##在所有setup_time中找出最小的
        first_delayedoff_time=min(next_delayedoff_time[:,0])
        # print(first_delayedoff_time,first_departure_time,first_setup_time_finished,next_arrival_time)
        ##least non_zero delayedoff_time
        ##四个event最小的时间，最先发生
        next_event_time=min(first_delayedoff_time,first_departure_time,first_setup_time_finished,next_arrival_time)
        ##找下一步应该离开还是到达
        if next_arrival_time==next_event_time:
            next_event_time=next_arrival_time
            next_event_type='arrival'
            # print('arrival')
        elif next_event_time==first_departure_time:
            next_event_type='departure'
            # print('departure')
        elif  next_event_time==first_setup_time_finished:
            next_event_type='setup_finished'
            # print('setup')
        elif next_event_time==first_delayedoff_time:
            next_event_type='delayedoff_expiry'
            # print('timeout')

        master_clock=next_event_time
        # print('masterclock:', master_clock)
        # print('marked:',marked,'\t','unmarked:',unmarked)
        # print('server_off_state:',servers_offs,'\t','server_setup_state:',next_setup_time,'server_busy_state:',servers_busy)
        #同时干三件事,第一，判断server里面是否有OFF的server
        ###如果有，就marked,并启动
        ##判断有没有DELAYEDOFF存在
        ##并且有OFF存在
        ##第一种情况，当一个job到达的时候
        if next_event_type=='arrival':
            ##至少有一个delayedoff
            # print('dispatcher', dispatcher, 'marked', marked, 'unmarked', unmarked)
            if min(next_delayedoff_time[:,0]) != float('inf'):
                p = 0
                max_delayedoff_time=0
                for q in range(len(next_delayedoff_time)):
                    if next_delayedoff_time[q] == float('inf'):
                        continue
                    if next_delayedoff_time[q] > max_delayedoff_time:
                        max_delayedoff_time = next_delayedoff_time[q]
                        p = q
                next_delayedoff_time[p] = float('inf')
                # print('选出非inf的最大的delayedoff，变为busy',next_delayedoff_time)
                servers_busy[p]=[next_arrival_time,next_service_time]
                next_departure_time[p]=master_clock+next_service_time
                # if next_departure_time[p]>end_time:
                #     return (response_time_cumulative_list, AA)


                # print('dispatcher', dispatcher, 'marked', marked, 'unmarked', unmarked)
                # print('BUSY',servers_busy)
                # print('Delayedoff:',next_delayedoff_time)
                ##没有一个delayedoff
            elif min(next_delayedoff_time[:,0])==float('inf'):
                # print('没有服务器delayedoff')
                ##检查是否有off存在
                if [1] in servers_offs[:,0]:
                    # print('有服务器是关的')
                    servers_offs_index=servers_offs.argmax(axis=0)
                    # print('找到任意一个关的服务器')
                    servers_offs[servers_offs_index]=0
                    # print('讲这个server打开',servers_offs)

                    next_setup_time[servers_offs_index]=setup_time+master_clock
                    # print('setup state',next_setup_time)
                    # print('将dispatcher最后一个，这个job marked')
                    dispatcher.append([next_arrival_time,next_service_time])
                    marked.append(dispatcher[-1])
                    # print('dispatcher',dispatcher,'marked',marked,'unmarked',unmarked)
                    # print('OFF',servers_offs,'\n','SETUP',next_setup_time)
                else:

                    # print('没有服务器关闭也没得在等待的，说明要么在busy，要么在setup')
                    dispatcher.append([next_arrival_time,next_service_time])
                    unmarked.append(dispatcher[-1])
                    # print('dispatcher',dispatcher,'marked',marked,'unmarked',unmarked)
                    # print('marked',marked,'unmarked',unmarked)
            # print('更新下一次到来的时间')
            if mode=='trace':
                index += 1
            if mode=='random':
                inter_arrival=- math.log(1 - random.random()) / arrival
                # ARR.append(inter_arrival)
                next_arrival_time = next_arrival_time +inter_arrival
                k1 = -math.log(1 - random.random()) / service
                k2 = -math.log(1 - random.random()) / service
                k3 = -math.log(1 - random.random()) / service
                next_service_time = k1 + k2 + k3






        if next_event_type=='departure':
            num_customer_served+=1
            first_departure_time_index=int(next_departure_time.argmin(axis=0))
            # print('最小的离开时间的位置',first_departure_time_index)
            # print('departure_time and corresponding arrival time',servers_busy[first_departure_time_index,0],next_departure_time[first_departure_time_index])
            if next_departure_time[first_departure_time_index]>end_time:
                # print(AA)
                # return (response_time_cumulative_list,AA,ARR)
                return (response_time_cumulative/num_customer_served,AA)
            AA.append((float('%5.3f'%servers_busy[first_departure_time_index,0]),float('%5.3f'%next_departure_time[first_departure_time_index])))
            next_departure_time[first_departure_time_index]=float('inf')
            # print('离开时间变为', first_departure_time, next_departure_time)

            response_time_cumulative = response_time_cumulative + master_clock - \
                                       servers_busy[first_departure_time_index,0]
            response_time_cumulative_list.append(response_time_cumulative/num_customer_served)
            servers_busy[first_departure_time_index] = [float('inf'), float('inf')]
            # print('BUSY:',servers_busy)
            if dispatcher==[]:
                # print('busy变为delayedoff')
                next_delayedoff_time[first_departure_time_index]=delayedoff_time+master_clock
                # print('BUSY',servers_busy)
                # print('Delayedoff:',next_delayedoff_time)
            else :
                # print('将queue里的第一个放进刚完成的这个busyserver里',servers_busy)
                # servers_busy_max_index = (servers_busy[:,1]).argmax(axis=0)
                if dispatcher[0] in unmarked:
                    servers_busy[first_departure_time_index]=dispatcher[0]
                    # print('BUSY:',servers_busy)
                    next_departure_time[first_departure_time_index] = master_clock+dispatcher[0][1]
                    # print('新的离开时间',next_departure_time)
                    if unmarked!=[]:
                        del unmarked[0]
                    if dispatcher!=[]:
                        del dispatcher[0]

                elif dispatcher[0] in marked:
                    servers_busy[first_departure_time_index] = dispatcher[0]
                    # next_departure_time_index=next_departure_time.argmax(axis=0)
                    next_departure_time[first_departure_time_index] = master_clock+dispatcher[0][1]
                    # print('新的离开时间',next_departure_time)
                    # AA.append((float(servers_busy[servers_busy_max_index,0]),float(next_departure_time[next_departure_time_index])))
                    if dispatcher!=[]:
                        del dispatcher[0]
                    if marked!=[]:
                        del marked[0]
                    if unmarked!=[]:
                        marked.append(unmarked[0])
                        # print('将unmarked，里面的第一个，变为marked，')
                        del unmarked[0]

                    else:
                        # print('将最大的建立时间变为inf')

                        max_setup_time=0
                        j=0
                        for i in range(len(next_setup_time)):
                            if next_setup_time[i]==float('inf'):
                                continue
                            elif next_setup_time[i]>max_setup_time:
                                max_setup_time=next_setup_time[i]
                                j=i
                        next_setup_time[j]=float('inf')
                        servers_offs[j]=[1]
                    # print('dispatcher', dispatcher, 'marked', marked, 'unmarked', unmarked)
                    # print('BUSY:',servers_busy)

                        # print('建立新的时间', next_setup_time)
        if next_event_type=='setup_finished':
            # print('服务器建立时间', next_setup_time)
            min_setup_time_index=next_setup_time.argmin(axis=0)
            # print('setup的时间变为0，变为busy')
            next_setup_time[min_setup_time_index]=float('inf')
            # print('服务器建立时间',next_setup_time)

            servers_busy[min_setup_time_index]=marked[0]

            next_departure_time[min_setup_time_index]=marked[0][1]+master_clock
            del marked[0]
            del dispatcher[0]
            # print('dispatcher', dispatcher, 'marked', marked, 'unmarked', unmarked)
            # print('BUSY:', servers_busy)
            # print('next_departure',next_departure_time)
        if next_event_type=='delayedoff_expiry':
            min_delayedoff_index=next_delayedoff_time.argmin(axis=0)
            next_delayedoff_time[min_delayedoff_index]=float('inf')
            servers_offs[min_delayedoff_index]=1
            # print('dispatcher', dispatcher, 'marked', marked, 'unmarked', unmarked)
            # print('Delayedoff:', next_delayedoff_time)
            # print('OFF:',servers_offs)
        # print(response_time_cumulative,num_customer_served)
    # if mode=='random':
        # del AA[-1]


    # print(AA)
    # return (response_time_cumulative_list,AA,ARR)
    # if AA[-1][1]>end_time:
    #     del AA[-1]
    return (response_time_cumulative/num_customer_served,AA)
##arrival 是一个parameter(the mean arrival of the jobs)

# Tc_range=np.arange(1000,200000,5000)
# mrt_list=[]
# L=[]
# K=[]
# for c in range(20):
# s=simulation(mode='random',arrival=0.35,service=1,m=5,setup_time=5,delayedoff_time=10,end_time=8000)
# print(s)
# bucket=[0]*(max(s[2])-min(s[2])+1)
# for i in range(len(s[2])):
#     bucket[s[2][i]-min(s[2])]+=1
#     B=[]
#     for i in range(len(bucket)):
#         if bucket[i]!=0:
#             B+=[i+min(s[2])]*bucket[i]
# print(B)
# L.append(s[1][0][0])
# for i in range(1,len(s[1])):
#     L.append(s[1][i][0]-s[1][i-1][0])
#     # print(i[0])
#      for i in range(0,len(s[1])+1):
#         L.append(i)
#      s[0].insert(0,0)
#      for i in range(2000):
#          del s[0][i]
#      print(sum(s[0])/len(s[0]))
#     print(sum(s[0])/len
# print(s[2])
#
# for i in range(len(s[2])):
#     L.append(i)
# print(list(df['Bin']))
# pl.plot(df['Bin'],df[0],linewidth=0.5,linestyle='-')
# # # pl.ylim(min(s[0])*1.01,max(s[0])*1.01)
# pl.show()