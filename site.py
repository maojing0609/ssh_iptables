#coding:UTF-8
#!/usr/bin/env python
from flask import Flask
from flask import request
import json
import os
from  Write_TO_Iptables import write2iptables

app = Flask(__name__)

@app.route('/get-local-ip',methods=['POST'])
def auth():
    data = request.get_data() ##获得字符串
    #print data
    if data == "3chgb02viLkkygu6okW3I3zxwoJEpz":
        ip = request.remote_addr
        if ip.strip() == os.popen("tail -n 1 /tmp/iplist").read().strip():
            pass
        else:
            os.popen("echo '%s' >> /tmp/iplist" %ip)
            #写到本机
            write2iptables(ip)
            #用ansible分发到其他服务器
            os.popen("/usr/bin/ansible yuyunservers_prod -m copy -a 'src=Write_TO_Iptables.py dest=/opt/Write_TO_Iptables.py'")
            os.popen("/usr/bin/ansible yuyunservers_prod -m script -a '/usr/bin/python /opt/Write_TO_Iptables.py %s'" %ip)
    else:
        print "GUN"
    return "hello"
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=9999,debug=True)


