#Data : 2021-7-12
#Author : wangyijie

import time
import requests
import json
import threading

def portal_model_request(id_str, url,headers,request_data, res_state_records,re_f):
    start_time = time.time()
    std_start_time=localtime = time.asctime( time.localtime(time.time()) )

    response = requests.post(url, data=json.dumps(request_data), headers=headers)

    res_code = str(response.status_code)
    if (res_state_records.__contains__(res_code)):
        res_state_records[res_code] += 1
    else:
        res_state_records["others"] += 1

    end_time = time.time()
    time_cost = end_time-start_time
    print(response.text)
    msg=response.text.split(",")[1].split(":")[1]
    print_info = "任务id:"+str(id_str)+"--返回状态码:" + res_code+"--消息:"+msg+"--耗时:"+str(time_cost)+"s--请求时间:"+str(std_start_time)+"\n"
    print(print_info)
    re_f.write(print_info)

if __name__ == '__main__':

    #请求次数
    request_times=300

    #每次请求并发个数
    request_counts=1

    #间隔睡眠时间
    sleep_time=2

    #模型执行请求的url
    url="https://geomodeling.njnu.edu.cn/task/invoke"
    #请求头信息，cookies！！！
    headers = {"Content-Type": "application/json; charset=UTF-8;",
    "Cookie":"_ga=GA1.3.1512668749.1625460558; Hm_lvt_10f0f9d6a8e84eea24952012709c66b0=1625532274,1626052916,1626087577,1626159320; JSESSIONID=F30461B6074F5D19C8BF1544BC52B362"
    }
    #post的数据（输入数据先上传至数据服务容器，获取url）
    request_data = {
    "inputs": [{
        "event": "LOADDATASET",
        "statename": "RUNSTATE",
        "suffix": "fds",
        "tag": "data11",
        "url": "http://221.226.60.2:8082/data/06604632-40eb-42e9-a61c-ceafa8f33262"
    }],
    "ip": "172.21.213.105",
    "oid": "fe6beeac-d4fa-4685-a7fa-3fc58dfb59d3",
    "pid": "51c650cd6320c08b54a71a0efa7b7d8a",
    "port": "8061",
    "key": "test123"
    }
    
    result_file=".\model_request_test_"+str(request_times)+"_"+str(request_counts)+".txt"
    task_id=0
    res_state_records = {"200": 0, "400": 0, "401": 0, "403": 0,"404": 0, "405": 0, "500": 0, "501": 0, "503": 0, "others": 0}

    print("正在测试中...")
    re_f = open(result_file, "w")
    re_f.write("目标模型:FDS\n")
    re_f.write("==================================\n")
    threads = []
    for i in range(0,request_times):
        for task_id in range(0, request_counts):
            t = threading.Thread(target=portal_model_request, args=(str(i)+"_"+str(task_id), url,headers,request_data, res_state_records,re_f,))
            threads.append(t)
            t.start()
        time.sleep(sleep_time)
    for t in threads:
        t.join()

    re_f.write("==================================\n")
    re_f.write("请求次数:{0}，每次请求个数:{1}".format(request_times,request_counts)+"\n")
    re_f.write("状态码返回记录:"+str(res_state_records)+"\n")
    re_f.close()
    print("状态码返回记录:"+str(res_state_records)+"\n")
    print("测试结束,结果请在文件中查看.")