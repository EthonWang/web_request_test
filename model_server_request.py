#Data : 2021-7-12
#Author : wangyijie

import threading
import time
from modelserver_sdk_python37 import *


# 根据ip和端口号建立连接
def getServerAccess(ip, port):
    # 初始化服务，ip和端口
    server = OGMSService.CreateServer(ip, port)
    status = server.connect()  # 判断链接状态
    if status:
        access = server.getServiceAccess()
        return access
    else:
        return -1

# 获取目标模型id
def getTargetModelid(access,target_model_name):
    list_ms = access.getModelServicesList()  # 获取模型列表
    target_model_index = -1  # 目标模型的位置
    for index, item in enumerate(list_ms):
        print("ID : {0}; Name : {1};  Type : {2}; index : {3}".format(
            item.id, item.name, item.type, index))
        if item.name == target_model_name:
            target_model_index = index  # 通过名字获取目标模型位置

    if target_model_index == -1:
        print("can not find your input moudle:"+target_model_name)
        return -1
    else:
        return list_ms[target_model_index].id

# 调用目标模型
def target_model_request(thread_id,access,target_model_id,model_data):
    time_start=time.time()

    # 上传数据
    # dataid = access.uploadDataByFile(
    #     "FDS_input_data", model_data)
    dataid="gd_8154a090-e2bf-11eb-b648-493ea92a0c14"
    # print("FDS_input_data - Input Data ID : {0}".format(dataid))
    touchair = access.getModelServiceByID(target_model_id)
    recordid = touchair.invoke([access.createDataConfigurationItem(
        "RUNSTATE", "LOADDATASET", dataid)])  # 向目标模型传入数据,调用模型
    
    record = access.getModelServiceRunningRecordByID(recordid)
    record.wait4Finished(8000)
    # print("FDS has been finished")
    # record.refresh()
    # for index, item in enumerate(record.outputs):
    #     dat = access.getDataByID(item.dataid)
    #     data_value = dat.value
    #     ext = data_value[data_value.find('.') + 1:]
    #     dat.save("E:\\temp_work\\web_request_test\\result_data\\" + item.eventname + '.' + ext)
    time_end=time.time()
    time_cost=time_end-time_start
    print("请求"+thread_id+"--模型运行耗时:"+str(time_cost)+"s")


if __name__ == '__main__':

    ip = "127.0.0.1"
    port = "8060"
    target_model_name = "FDS"
    model_data = "E:\\temp_work\\web_request_test\\test_data\\data11.fds"

    access = getServerAccess(ip, port)  # 获取模型服务容器进程

    target_model_id=-1
    if access != -1:
        target_model_id=getTargetModelid(access,target_model_name)

    # if target_model_id!=-1:
    #     target_model_request(access,target_model_id,model_data)

    print("正在执行")
    
    # thread_id="1"
    # target_model_request(thread_id,access,target_model_id,model_data)


    for count in range(0,1):
        for t_id in range(0,30):
            t = threading.Thread(target=target_model_request,args=(str(t_id),access,target_model_id,model_data,))
            t.start()
    

