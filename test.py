import communication
import os
import subprocess
import time


 Uzyyj thread i poszukaj jak się mają komunikować
if __name__ == "__main__":
    code = """
    import communication
    srv = communication.Server('localhost')
    srv.start()
    """
   # p1 = subprocess.run(['py', code],capture_output=True, encoding='UTF-8')
    
    #cmd = "ps -A|grep 'process_name'"
    ps = subprocess.Popen(code,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    time.sleep(1) 
    
    
    communication.Client.sendMesseng('localhost','test2022')
    #print('Server posiada w buforze', srv.msgBuffor)
    #print(p1.stdout)
    time.sleep(1) 
    output = ps.communicate()[0]
    print(output)
