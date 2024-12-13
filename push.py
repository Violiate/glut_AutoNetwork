import smtplib
import requests,json,re,sys
from loguru import logger
from i18n import *
#from globals import load_config

class PUSH():
    def __init__(self,config):
        self.config = config
        self.title="网络配置变更通知"
        self.headers = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
         }
        if 'dingding_token' in config:
            self.dingding_token=config['dingding_token']
        else:
            self.dingding_token=''
        if 'pushplus_token' in config:
            self.pushplus_token=config['pushplus_token']
        else:
            self.pushplus_token=''
        if 'smtp_mail_host' in config:
            self.smtp_mail_host=config['smtp_mail_host']
        else:
            self.smtp_mail_host=""
        if 'smtp_mail_user' in config:
            self.smtp_mail_user=config['smtp_mail_user']
        else:
            self.smtp_mail_user=""
        if 'smtp_mail_pass' in config:
            self.smtp_mail_pass=config['smtp_mail_pass']
        else:
            self.smtp_mail_pass=""
        if 'smtp_sender' in config:
            self.smtp_sender=config['smtp_sender']
        else:
            self.smtp_sender=""
        if 'smtp_receivers' in config:
            self.smtp_receivers=config['smtp_receivers']
        else:
            self.smtp_receivers=""
        if 'bark_token' in config:
            self.bark_token=config['bark_token']
        else:
            self.bark_token=""
        if 'ftqq_token' in config:
            self.ftqq_token=config['ftqq_token']
        else:
            self.ftqq_token=""
        if 'wx_token' in config:
            self.wx_token=config['wx_token']
        else:
            self.wx_token=""
        
                  
    def push(self,message):
        self.message = message
        if self.dingding_token!='':
            self.ding_push()
        if self.ftqq_token:
            self.ftqq()
        if self.wx_token:
            self.wx_push()  
        if self.pushplus_token!='':
            self.pushplus()
        if self.bark_token!='':
            self.bark() 
        if self.smtp_mail_host and self.smtp_mail_pass and self.smtp_sender : 
            self.smtp()
        

    def ding_push(self):
        url=f"https://oapi.dingtalk.com/robot/send?access_token={self.dingding_token}"
        # 构建请求数据
        msg = {
        "msgtype": "text",
        "text": {
            "content": self.message
        },
        "at": {
            "isAtAll": False
        }
        }
        # 对请求的数据进行json封装
        message_json = json.dumps(msg)
        # 发送请求
        info = requests.post(url, data=message_json, headers=self.headers)
        # 打印返回的结果
        if info.json()['errcode'] == 0:
            #logger.info(i18n_format("dingding_send_success"))
            logger.info("dingding_send_success")
        else:
            logger.info(info.text)
        
    def pushplus(self):
       
      
      token = self.pushplus_token #在pushpush网站中可以找到
      
      url = 'http://www.pushplus.plus/send'
      data = {
        "token":token,
        "title":self.message,
        "content":self.message
      }
      
      try:
        info=requests.post(url, json=data,headers=self.headers)
        logger.debug(info.text)
        #logger.info(i18n_format("pushplus_send_success"))
        logger.info("pushplus_send_success")
      except Exception as e:
        logger.error(e)
      
    def ftqq(self):
        data={
            "title":self.title,
            "desp":self.message,
            "noip":1
        }
        url=f"https://sctapi.ftqq.com/{self.ftqq_token}.send"
        try:
         info=requests.post(url, data=data,headers=self.headers)
         logger.debug(info.text)
         #logger.info(i18n_format("ftqq_send_success"))
         logger.info("bark_send_success")
        except Exception as e:
            logger.error(e)
        


    def wx_push(self):
        url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={self.wx_token}'
        data = {
          'msgtype': 'text',
          'text': {
              'content': self.message
             }
          }
        try:
            info=requests.post(url, json=data,headers=self.headers)
            logger.debug(info.text)
            #logger.info(i18n_format("wx_send_success"))
            logger.info("wx_send_success")
        except Exception as e:
            logger.error(e)
        


    def smtp(self):
        from email.mime.text import MIMEText
        #设置服务器所需信息
        #163邮箱服务器地址
        mail_host = self.smtp_mail_host 
        #163用户名
        mail_user = self.smtp_mail_user  
        #密码(部分邮箱为授权码) 
        mail_pass = self.smtp_mail_pass   
        #邮件发送方邮箱地址
        sender = self.smtp_sender  
        #邮件接受方邮箱地址，注意需要[]包裹，这意味`着你可以写多个邮件地址群发
        receivers = list(self.smtp_receivers.split(","))  

        #设置email信息
        #邮件内容设置
        message = MIMEText(self.message,'plain','utf-8')
        #邮件主题       
        message['Subject'] = self.title 
        #发送方信息
        message['From'] = sender 
        
        #接受方信息 
        for receiver in receivers:
          message['To'] = receiver    
        

          #登录并发送邮件
          try:
            smtpObj = smtplib.SMTP() 
            #连接到服务器
            smtpObj.connect(mail_host,25)
            #登录到服务器
            smtpObj.login(mail_user,mail_pass) 
            #发送
            smtpObj.sendmail(
                sender,receivers,message.as_string()) 
            #退出
            smtpObj.quit() 
            #logger.info(i18n_format("smtp_send_success"))
            logger.info("send_success")
          except smtplib.SMTPException as e:
            logger.error(e) #打印错误
            
        
    def bark(self):
        data={
            "title":self.title,
            "body":self.message,
            "level":"timeSensitive",
            #推送中断级别。 
#active：默认值，系统会立即亮屏显示通知
#timeSensitive：时效性通知，可在专注状态下显示通知。
#passive：仅将通知添加到通知列表，不会亮屏提醒。"""   
            "badge":1,
            "icon":"https://ys.mihoyo.com/main/favicon.ico",
            "group":"NET", 
            "isArchive":1
        }
        url=f'https://api.day.app/{self.bark_token}'
        try:
          info=requests.post(url,json=data)
          logger.info("bark_send_success")
          #logger.debug(info.text)
          #logger.info(i18n_format("bark_send_success"))
        except Exception as e:
          logger.error(e)

if __name__ == "__main__":
    config={}
    message = sys.argv[1] if len(sys.argv) > 1 else "消息出错，空消息！"
    pusher=PUSH(config)
    PUSH.push(pusher,message)