#coding:UTF-8
#!/usr/bin/env python
from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
from flask import Flask, request, g
import json
import os
from  Write_TO_Iptables import write2iptables

app = Flask(__name__)
app.config.update(DEBUG=True)

@app.route('/get-local-ip',methods=['POST'])
def auth():
    data = request.get_data() ##获得字符串
    #print data
    if data == "3chgb02viLkkygu6okW3I3zxwoJEpz":
        ip = request.remote_addr[7:]
        print ip
        if ip.strip() == os.popen("tail -n 1 /tmp/iplist").read().strip():
            pass
        else:
            os.popen("echo '%s' >> /tmp/iplist" %ip)
            #写到本机
            print ip
            write2iptables(ip)
            #用ansible分发到其他服务器
            os.popen("/usr/bin/ansible yuyunservers_prod -m copy -a 'src=/root/whitelist/Write_TO_Iptables.py dest=/opt/Write_TO_Iptables.py'")
            os.popen("/usr/bin/ansible yuyunservers_prod -m script -a '/usr/bin/python /opt/Write_TO_Iptables.py %s'" %ip)
    else:
        print "GUN"
    return "hello"
@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    http_server = WSGIServer(('', 9999), app)
    http_server.serve_forever()
