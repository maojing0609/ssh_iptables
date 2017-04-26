#!/usr/bin/env python
# coding=utf-8
import requests
import json
import sys
import ConfigParser
class weChat:
    def __init__(self,Corpid,Secret):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (Corpid,Secret)
        res = self.url_req(url)
        self.token = res["access_token"]
    def url_req(self,url):
        req = requests.get(url)
        res = json.loads(req.text)
        return res

    def send_message(self,user,content):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % self.token
        data = {
                "touser": user,
                "msgtype": "news",
                "agentid": 1,
               "news": {
               "articles":[
                   {
               "title": "ssh-iptables-notice",
               "description": content,
                   }
                  ]
                }
        }
        data = json.dumps(data,ensure_ascii=False)
        res = requests.post(url,data)
        if json.loads(res.content)['errmsg'] == 'ok':
            return "send message sucessed"
        else:
            return res


if __name__ == '__main__':
    user = sys.argv[1]
    args = sys.argv
    content = ' '.join(args[2:])
	config_file = os.path.join(sys.path[0],'config.ini')
    cp = ConfigParser.SafeConfigParser()
    cp.read(config_file)
    id = cp.get('wx','id')
    Secret = cp.get('wx','Secret')
    receiver = cp.get('wx','receiver')
    get_token = weChat(id,Secret)
    get_token.send_message(user,content)
