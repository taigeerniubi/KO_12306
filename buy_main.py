from DrissionPage import ChromiumPage,ChromiumOptions
from DrissionPage.common import Actions
from DrissionPage.common import Keys
import os
from dotenv import load_dotenv,find_dotenv
from pypinyin import pinyin,Style # 拼音转换库
import requests
import json

# 定义一个函数，将中文转换为拼音
def yuyan(chinese):
    zw = pinyin(chinese, style=Style.NORMAL)  # 获取首字母
    string = ''.join([i[0] for i in zw])
    return string
# 12306购票脚本
def buy(Chufa,Daoda,Time,Xuanze):
    load_dotenv(find_dotenv())
    # 自动打开浏览器
    options = ChromiumOptions()
    # 设置edge浏览器路径
    options.set_browser_path(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
    zdh = ChromiumPage(options)
    # 自动定位控制鼠标
    dzl = Actions(zdh)
    # 自动打开网站 
    zdh.get(f'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E5%8C%97%E4%BA%AC,BJP&ts=%E4%B8%8A%E6%B5%B7,SHH&date=2025-06-25&flag=N,N,Y')
    # 出发地元素定位
    zdh.ele('css:#fromStationText').clear() # 清空输入框
    dzl.move_to('css:#fromStationText').click().type(yuyan(Chufa))
    zdh.ele('css:#fromStationText').input(Keys.ENTER) #回车
    # 到达地元素定位
    dzl.move_to('css:#toStationText').click().type(yuyan(Daoda))
    zdh.ele('css:#toStationText').input(Keys.ENTER)
    # 出发时间元素定位
    zdh.ele('css:#train_date').clear() # 清空输入框·
    zdh.ele('css:#train_date').input(Time)  # 输入出发时间·
    # 搜索按钮元素定位
    zdh.ele('css:#query_ticket').click()

    # 预定按钮元素定位
    zdh.ele(f'css:#queryLeftTable tr:nth-child({int(Xuanze)*2-1}) .btn72').click() #伪类选择器选择表格table的第(Xuanze)*2-1行的标签
    login = zdh.ele('css:#login_user').text  # 登录元素定位
    if login == '登录':
        # 账号登录定位
        zdh.ele('css:#J-userName').input(os.environ['USERNAME'])  # 替换为你的用户名
        zdh.ele('css:#J-password').input(os.environ['PASSWORD'])  # 替换为你的密码     
        # 登录按钮元素定位
        zdh.ele('css:#J-login').click()
        # 短信验证
        dzl.move_to('css:#fid_card').click().type(os.environ['YZM'])  # 后四位
        # 获取验证码按钮
        zdh.ele('css:#verification_code').click()
        # 用户输入验证码
        yzm = input('请输入验证码：')  
        zdh.ele('css:#code').input(yzm)
        # 提交按钮元素定位
        zdh.ele('css:#sureClick').click()
    else:
        print('已登录，无需再次登录') 



# 导入城市json
k = open('city.json',encoding='utf-8').read()
# 将json字符串转换为字典
city = json.loads(k)
# print(city)
chufa = input('请输入出发城市：')
daoda = input('请输入到达城市：')
times= input('请输入出发时间(格式为2025-06-25)：')
url = (
    f'https://kyfw.12306.cn/otn/leftTicket/queryU?'
    f'leftTicketDTO.train_date={times}&'
    f'leftTicketDTO.from_station={city[chufa]}&'
    f'leftTicketDTO.to_station={city[daoda]}&purpose_codes=ADULT'
)
headers = {
    'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/137.0.0.0',
    'cookie': '_uab_collina=175083699545972560948741; JSESSIONID=6EBC23425C2ED650EFCB9B0BD9C59BA6; tk=8n_Lv_L42w5i31bcfpyTDEWDLk6AMlAOdjPQkzK6hKYzim1m0; BIGipServerotn=1608057098.24610.0000; BIGipServerpassport=870842634.50215.0000; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; route=495c805987d0f5c8c84b14f60212447d; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_fromDate=2025-06-25; _jc_save_toDate=2025-06-25; _jc_save_wfdc_flag=dc; uKey=cee2ddbc5e66a1360671faf171ac121bd30168e583dc3429c785708ce18d1ac4',
    'referer': 'https://kyfw.12306.cn/otn/leftTicket/init?'
}

# 发起请求
response = requests.get(url, headers=headers)
# 解析响应内容
JOSN = response.json()
data = JOSN['data']['result']
id = 0  # 序号
for i in data:
    index = i.split('|')
    page = 0
    for j in index:
        # print(j,'---序号是',page)
        page +=1
    checi = index[3]  #车次
    go_time = index[8]  #出发时间
    out_time = index[9] #到达时间
    time = index[10] #历时
    vip = index[32] #商务座
    ydz = index[31] #一等座
    edz = index[30] #二等座
    day = index[13]  #日期
    id += 1  # 序号自增
    dit = {
        '序号':id,
        '车次': checi,
        '出发时间': go_time,
        '到达时间': out_time,
        '历时': time,
        '商务座': vip,
        '一等座': ydz,
        '二等座': edz,
        '日期': day
    }
    print(dit)
xuanze = input('选择几号车次，请输入序号： ')
if __name__ == "__main__":
    buy(chufa,daoda,times,xuanze)