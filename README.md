# ssh_iptables
#环境
centos:6.5 7
python 2.7
flask 0.12.1
ansible 2.2.1

1、使用场景
线上服务器的ssh端口直接暴露在公网，且iptables的source没有做限制(对于那种拨号上网的同学)，如果你的Ip变了，可以直接向接口传数据达到自动添加iptables策略
实现有效的过滤


2、使用步骤
  a、服务端安装flask,ansible
  b、启动site.py
  c、配置ansible
  
  客户端只需要 curl -d "3chgb02viLkkygu6okW3I3zxwoJEpzddd" http://IP:PORT/get-local-ip
  就可以将自己的IP发送给服务端，然后你就可以ssh到集群了
