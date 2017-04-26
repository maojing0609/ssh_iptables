#coding:UTF-8
#!/usr/bin/env python
from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
from flask import Flask, request, g
import json
import os,sys
import mylog
from  Write_TO_Iptables import write2iptables
import ConfigParser

#config_file = os.path.join('/root/whitelist','config.ini')
config_file = os.path.join(sys.path[0],'config.ini')
cp = ConfigParser.SafeConfigParser()
cp.read(config_file)
mykey = cp.get('pass','data')
port = int(cp.get('flask_port','port'))

app = Flask(__name__)
app.config.update(DEBUG=False)

@app.route('/get-local-ip',methods=['POST'])
def auth():
    try:
        data = request.get_data() ##获得字符串
        ip = request.remote_addr[7:]
        #print data
        if data == mykey:
            if ip.strip() == os.popen("tail -n 1 /tmp/iplist").read().strip():
                mylog.logging.warn('%s already in iptables,no need to add!!!' %ip)
                pass
            else:
                os.popen("echo '%s' >> /tmp/iplist" %ip)
                #写到本机
                write2iptables(ip)
                mylog.logging.info('SUCCESS ADD %s to MANARGER' %ip)
                #用ansible分发到其他服务器
                os.popen("/usr/bin/ansible yuyunservers_prod -m copy -a 'src=/root/whitelist/Write_TO_Iptables.py dest=/opt/Write_TO_Iptables.py'")
                result = os.system("/usr/bin/ansible yuyunservers_prod -m script -a '/usr/bin/python /opt/Write_TO_Iptables.py %s'" %ip)
                if result == '0':
                    mylog.logging.info('SUCCESS ADD %s to CloudServer' %ip)
                else:
                    mylog.logging.error('FAILED TO ADD %s to CloudServer!!!PLEASE CHECK!!!!!!!' %ip)

        else:
            mylog.logging.warning('wrong client %s with error pass!!!' %ip)
        return "200"
    except Exception,e:
        mylog.logging.error(e)
        sys.exit()
@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    http_server = WSGIServer(('', port), app)
    http_server.serve_forever()

