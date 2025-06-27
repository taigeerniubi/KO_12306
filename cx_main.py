import requests
import json
# 导入城市json
k = open('city.json',encoding='utf-8').read()
# 将json字符串转换为字典
city = json.loads(k)
# print(city)
chufa = input('请输入出发城市：')
daoda = input('请输入到达城市：')
time= input('请输入出发时间(格式为2025-06-25)：')
url = (
    f'https://kyfw.12306.cn/otn/leftTicket/queryU?'
    f'leftTicketDTO.train_date={time}&'
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
# print(data)
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