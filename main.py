import time

import pymysql
import win32api
import win32con
import win32gui
from selenium import webdriver

from explicit_wait import explicit_wait
from ins_pymsql import fetch_one_sql, oprt_mysql



class Main():
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306,
                                    user='root', password='123456',
                                    db='xy_test', charset='utf8')
        #上传图片路径
        self.filepath = "C:\\Users\\hu\\Desktop\\xy-text\\ceshi_pic.png"
        
    def ins_phone_opr(self,email,pwd,filepath):
        mobileEmulation = {"deviceName":"Galaxy S5"}
        options = webdriver.ChromeOptions()
        options.add_experimental_option('mobileEmulation', mobileEmulation)
        options.add_argument("-lang=en-uk")
        chrome_obj = webdriver.Chrome(chrome_options=options)
        chrome_obj.maximize_window()
        chrome_obj.get('https://www.instagram.com/accounts/login/')
        ec_params = ['//form[@method="post"]',"XPath"]
        explicit_wait(chrome_obj,"VOEL",ec_params)
        chrome_obj.find_element_by_xpath('//input[@name="username"]').send_keys(email)
        chrome_obj.find_element_by_xpath('//input[@name="password"]').send_keys(pwd)
        chrome_obj.find_element_by_xpath('//form//button[@type="submit"]').click()
        try:
            # 登录成功 1
            # 处理弹出窗口
            ec_params = ['//div/div[3]/button[2]',"XPath"]
            explicit_wait(chrome_obj,"VOEL",ec_params)
            chrome_obj.find_element_by_xpath('//div/div[3]/button[2]').click()
            print("Login successful!")
            sql = "update account set state=1,log_num=log_num+1 where email=%s;"
            oprt_mysql(self.conn,sql,email)
        except:
            try:
                #密码错误 2
                chrome_obj.find_element_by_xpath('//div/div[2]/button').click()
                print("Password mistake!")
                sql = "update account set state=2,log_num=log_num+1 where email=%s;"
                oprt_mysql(self.conn,sql,email)
                chrome_obj.quit()
            except :
                #账户错误 2
                login_flag = chrome_obj.find_element_by_xpath('//form//div/p[@id="slfErrorAlert"]').text
                print("Login failed："+login_flag)
                sql = "update account set state=2,log_num=log_num+1 where email=%s;"
                oprt_mysql(self.conn,sql,email)
                chrome_obj.quit()

        try:
            # 点击发表动态
            chrome_obj.find_element_by_xpath('//div[@role="menuitem"]/span').click()
        except :
            pass
        time.sleep(3)

        # 窗口类名
        classname = "#32770"
        # 窗口句柄
        ck_ju = win32gui.FindWindow(classname,"打开")
        # ck_ju = win32gui.FindWindow(classname,"Open")
        ComboBoxEx32 = win32gui.FindWindowEx(ck_ju, 0, 'ComboBoxEx32', None)
        ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
        # 输入框句柄
        Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)
        # 输入路径
        win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None, filepath)
        time.sleep(3)

        win32api.keybd_event(13, 0, 0, 0)
        win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
        
        try:
            # 下一步
            ec_params = ['//header/div/div[2]/button',"XPath"]
            explicit_wait(chrome_obj,"VOEL",ec_params)
            chrome_obj.find_element_by_xpath('//header/div/div[2]/button').click()      
        except:
            pass
        time.sleep(3)
        try:
            # 分享
            ec_params = ['//header/div/div[2]/button',"XPath"]
            explicit_wait(chrome_obj,"VOEL",ec_params)
            chrome_obj.find_element_by_xpath('//header/div/div[2]/button').click()
            sql = "update account set fb_num=fb_num+1 where email=%s;"
            oprt_mysql(self.conn,sql,email)
        except:
            pass
        time.sleep(3)

        try:
            # 处理弹出窗口
            chrome_obj.find_element_by_xpath('//div/div[3]/button[2]').click()
        except:
            pass
        
        chrome_obj.quit()

    def ins_opr(self,email,pwd,kh_name):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("-lang=en-uk")
            chrome_obj = webdriver.Chrome(chrome_options=options)
            chrome_obj.maximize_window()
            chrome_obj.get("https://www.instagram.com/accounts/login/")
            ec_params = ['//form[@method="post"]',"XPath"]
            explicit_wait(chrome_obj,"VOEL",ec_params)
            chrome_obj.find_element_by_xpath('//input[@name="username"]').send_keys(email)
            chrome_obj.find_element_by_xpath('//input[@name="password"]').send_keys(pwd)
            chrome_obj.find_element_by_xpath('//form//button[@type="submit"]').click()
            try:
                # 登录成功 1
                # 点击弹出窗口 以后再说（打开通知）
                ec_params = ['//div/button[@tabindex="0"][2]',"XPath"]
                explicit_wait(chrome_obj,"VOEL",ec_params)
                chrome_obj.find_element_by_xpath('//div/button[@tabindex="0"][2]').click()
                print("Login successful!")
                sql = "update account set state=1,log_num=log_num+1 where email=%s;"
                oprt_mysql(self.conn,sql,email)
            except:
                #输出登录失败原因 2
                login_flag = chrome_obj.find_element_by_xpath('//form//div/p[@id="slfErrorAlert"]').text
                print("Login failed："+login_flag)
                sql = "update account set state=2,log_num=log_num+1 where email=%s;"
                oprt_mysql(self.conn,sql,email)
                chrome_obj.quit()
        except:
            print("The login timeout!")


        # 获取账户名称      
        try:
            my_name = chrome_obj.find_element_by_xpath('//div[@role="button"]/../div[2]/div/a').text
            print("Account name:" + my_name)
            sql = "update account set uname=%s where email=%s;"
            oprt_mysql(self.conn,sql,(my_name,email))
        except:
            pass

        #点赞，收藏，评论功能
        try:
            # 点击进入主页
            chrome_obj.find_element_by_xpath('//div/a[@href="/explore/"]/span').click()
            print("Enter the main page!")
        except:
            pass

        try:
            # 点击第一张图片
            pic_xpath = '//main[@role="main"]/div/article/div/div/div[1]/div[1]/a/div/div[2]'
            ec_params = [pic_xpath,"XPath"]
            explicit_wait(chrome_obj,"VOEL",ec_params)
            chrome_obj.find_element_by_xpath(pic_xpath).click()
        except:
            print("Load home page timeout!")

        # 循环50张图片
        for i in range(50):
            # 获取发布者名称
            ec_params = ['//header//h2/a',"XPath"]
            explicit_wait(chrome_obj,"VOEL",ec_params)
            Ins_name = chrome_obj.find_element_by_xpath('//header//h2/a').text
            print("The publisher:"+Ins_name)

            if Ins_name in kh_name:
                # 点赞
                zan = chrome_obj.find_element_by_xpath('//section/span[1]/button/span').get_attribute("aria-label")
                if zan == "Like":
                    chrome_obj.find_element_by_xpath('//section/span[1]/button/span').click()
                    sql = "update account set dz_num=dz_num+1 where email=%s;"
                    oprt_mysql(self.conn,sql,email)
                # 收藏
                sc = chrome_obj.find_element_by_xpath('//section/span[4]/button/span').get_attribute("aria-label")
                if sc == "Save":
                    chrome_obj.find_element_by_xpath('//section/span[4]/button/span').click()
                    sql = "update account set sc_num=sc_num+1 where email=%s;"
                    oprt_mysql(self.conn,sql,email)
                # 评论
                # 所有评论者名单
                pl_xpath = chrome_obj.find_elements_by_xpath('//div[@role="button"]//../ul//h3/a')
                pl_name = []
                for i in pl_xpath:
                    pl_name.append(i.text)
                if my_name in pl_name:
                    print("You have commented!")
                else:
                    # 发表评论
                    pl_content = "Beautiful pictures!"
                    chrome_obj.find_element_by_xpath('//section/div/form/textarea').click()
                    chrome_obj.find_element_by_xpath('//section/div/form/textarea').send_keys(pl_content)
                    chrome_obj.find_element_by_xpath('//form//button[@type="submit"]').click()
                    time.sleep(3)
                    sql = "update account set pl_num=pl_num+1 where email=%s;"
                    oprt_mysql(self.conn,sql,email)
                
            # 判断是否为第一页
            xpth_num = chrome_obj.find_elements_by_xpath('//div[@class="D1AKJ"]/a')
            # 点击下一页
            if len(xpth_num) == 1:
                chrome_obj.find_element_by_xpath('//div[@class="D1AKJ"]/a').click()
            else:
                chrome_obj.find_element_by_xpath('//div[@class="D1AKJ"]/a[2]').click()

        chrome_obj.quit()
    
    def run(self):
        # 需要点赞客户的昵称
        sql = "select * from kh_name"
        date = fetch_one_sql(self.conn,sql)
        kh_name = []
        for i in date:
            kh_name.append(i[1])
        # 循环找出客户邮箱与密码
        sql = "select * from account"
        account = fetch_one_sql(self.conn,sql)
        for acc in account:
            acc_email = acc[1]
            acc_pwd = acc[2]
            self.ins_phone_opr(acc_email,acc_pwd,self.filepath)
            self.ins_opr(acc_email,acc_pwd,kh_name)

if __name__ == "__main__":
    Run = Main()
    Run.run()
