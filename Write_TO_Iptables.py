#coding:utf-8
#!/usr/bin/env python
import os
import sys
def write2iptables(ip):
#将ssh端口状态为ACCEPT，且源地址是0.0.0.0全部DROP，只将客户端传递过来的IP加到INPUT
    ssh_port = os.popen("cat /etc/ssh/sshd_config|grep 'Port '|awk -F ' ' {'print $2'}").read()
    n = 0
    for i in os.popen('iptables -L -n --line|grep ACCEPT|grep "dpt:%s"|awk -F " " {"print \$1,\$5"}' %ssh_port):
        #print "i:%s" %i
        n = n + 1
        if i.find("0.0.0.0") != -1:
            #print "iptables line is %s" % i[0:2].strip(' ')
            if n == 1:
                os.popen('iptables -D INPUT %s' % str(int(i[0:2].strip(' '))))
            else:
                os.popen('iptables -D INPUT %s' % str(int(i[0:2].strip(' '))-1))
        else:
            break
    os.popen("iptables -I INPUT 1 -s %s -p tcp --dport %s -j ACCEPT" %(ip,ssh_port))

if __name__ == "__main__":
    ip = sys.argv[1]
    write2iptables(ip)
