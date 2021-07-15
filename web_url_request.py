#Data : 2021-7-12
#Author : wangyijie

import sys
import time
import requests
import threading

def web_request(task_id,url,res_state_records,re_f):
    start_time = time.time()

    response = requests.get(url)
    res_code=str(response.status_code)

    if (res_state_records.__contains__(res_code)):
        res_state_records[res_code]+=1 
    else:
        res_state_records["others"]+=1

    end_time = time.time()
    time_cost=end_time-start_time
    print_info="请求任务id:"+str(task_id)+"---返回状态码:"+res_code+"---耗时:"+str(time_cost)+"s\n"
    re_f.write(print_info)

if __name__ == '__main__':

    #单次并发请求次数,默认100
    request_times=100 

    #目标网址,默认为OpenGMS门户官网
    target_url="https://geomodeling.njnu.edu.cn/"
    if(len(sys.argv)>=2):
        target_url=sys.argv[1]
    if(len(sys.argv)==3):
        request_times=sys.argv[2]

    #opengms官网网址 1
    opengms_portal_url = "https://geomodeling.njnu.edu.cn/"
    #opengms官网模型仓库网址 2
    opengms_repository_url="https://geomodeling.njnu.edu.cn/modelItem/repository"
    #opengms官网SWAT模型网址 3
    swat_model_url="https://geomodeling.njnu.edu.cn/modelItem/3f6857ba-c2d2-4e27-b220-6e5367803a12"
    #opengms官网FDS模型调用地址 4
    FDS_invoke_url="https://geomodeling.njnu.edu.cn/task/fe6beeac-d4fa-4685-a7fa-3fc58dfb59d3"

    #相应信息结果输出文件
    result_file=".\web_request_test_"+str(request_times)+".txt"
    
    re_f=open(result_file,"w")

    print("正在测试中...")
    
    web_urls=[opengms_portal_url,opengms_repository_url,swat_model_url,FDS_invoke_url]
    web_urls_names=["opengms门户","模型仓库","SWAT模型页面","FDS模型调用页面",]
    for index,target_url in enumerate(web_urls):
        res_state_records={"200":0,"400":0,"401":0,"403":0,"404":0,"405":0,"500":0,"501":0,"503":0,"others":0}
        re_f.write("id:"+str(index)+" 目标网址内容:"+web_urls_names[index]+"\n")
        re_f.write("目标网址:"+target_url+"\n")
        re_f.write("==================================\n")
        threads = []
        for task_id in range(0,int(request_times)):
            t = threading.Thread(target=web_request,args=(task_id,target_url,res_state_records,re_f,)) 
            threads.append(t)
            t.start()   
        for t in threads: 
            t.join()
        
        re_f.write("==================================\n")
        re_f.write("总请求次数:{0}".format(request_times)+"\n")
        re_f.write("状态码返回记录:"+str(res_state_records)+"\n\n\n")

    re_f.close()
    print("测试结束,结果请在文件中查看.")
