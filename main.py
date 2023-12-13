import random
from time import time, localtime

import requests
from bs4 import BeautifulSoup

import cityinfo
from requests import get, post
from datetime import datetime, date
from zhdate import ZhDate
import sys
import os


def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)


def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token


def get_weather(province, city):
    # 城市id
    try:
        city_id = cityinfo.cityInfo[province][city]["AREAID"]
    except KeyError:
        print("推送消息失败，请检查省份或城市是否正确")
        os.system("pause")
        sys.exit(1)
    # city_id = 101280101
    # 毫秒级时间戳
    t = (int(round(time() * 1000)))
    headers = {
        "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(city_id),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = "http://d1.weather.com.cn/dingzhi/{}.html?_={}".format(city_id, t)
    response = get(url, headers=headers)
    response.encoding = "utf-8"
    response_data = response.text.split(";")[0].split("=")[-1]
    response_json = eval(response_data)
    print(response_json)
    weatherinfo = response_json["weatherinfo"]
    # 天气
    weather = weatherinfo["weather"]
    # 最高气温
    temp = weatherinfo["temp"]
    # 最低气温
    tempn = weatherinfo["tempn"]

    ##===================================================================================
    headers1 = {
        "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(city_id),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    HTML = "https://tianqi.2345.com/pudong1d/71146.htm"

    response1 = requests.get(HTML, headers=headers1)
    response1.encoding = "utf-8"
    my_soup = BeautifulSoup(response1.text, "html.parser")

    # 获取信息主标签
    main_str = my_soup.find("div", attrs={"class": "real-mess"})

    # 获取今天天气、温度
    # weather_main = main_str.find("div", attrs={"class": "real-today"})
    # split = weather_main.text.split("：")[1]
    # # 今天天气
    # weather = split.split("° ")[1]
    # # 最高气温
    # temp = split.split("° ")[0].split("-")[1] + "°C"
    # # 最低气温
    # tempn = split.split("° ")[0].split("-")[0] + "°C"

    # 现在的天气 多云
    now_weather = main_str.find("em", attrs={"class": "cludy"}).text
    find_all = main_str.findAll("span", attrs={"class": "real-data-mess fl"})
    # 当前风向 东北风3级
    wind_direction = find_all[0].text.replace(' ', '')
    # 当前空气湿度 86%
    air_humidity = find_all[1].text.replace('湿度 ', '')
    # 当前紫外线  很弱
    ultraviolet_rays = find_all[2].text.replace('紫外线 ', '')

    # 空气主要标签
    air_main = my_soup.find("div", attrs={"class": "box-mod-tb"})
    # 空气质量  优-16
    air_quality = air_main.find("em").text + "-" + air_main.find("span").text
    # pm 2.5    10
    pm = air_main.find("div", attrs={"class": "aqi-map-style-tip"}).find("em").text

    hours24_main = my_soup.find("div", attrs={"class": "hours24-data-th-right"})
    # 日出时间  06:01
    sunrise = hours24_main.findAll("span")[0].text.split(" ")[1]
    # 日落时间  19:00
    sunset = hours24_main.findAll("span")[1].text.split(" ")[1]

    str_all = """幸福总是在不经意间降临，你需要静静地以一颗平常心去感受。
我不知道结局怎样，我现在很幸福就可以了。
黄晕的光，扯出零星的幸福。
在背水一战之后，爱情终于迎来了晴空朗朗的明艳幸福，而你也让我觉欣喜。
我还是一样的爱着你，等待的幸福更不需要怀疑，我永远都愿意一直这样爱着你。
在我的心里，唯独剩下的只有曾经那份天真的幸福，可爱的笑脸。
爱自我爱的人本身就是一种幸福，你能够记住过去的完美。
爱也是一种担当，真爱承担着两颗灵魂的重量。所以，爱情不是同情。不爱，一定不要缠绵和纠缠，那样的破碎，不但有痛，更多的是伤。我不想再痛，更不想伤人。
我希望的是：未来的路上一半有你在就好！
读过一些书，才知道财富；过了一辈子，才知道幸福。
人生暮年，最大的幸福莫过于有你一直陪着我。
我比世界上任何人都希望你幸福，但假如最后让你幸福的人不是我，我依然也只是希望你幸福就好啦。
望回廊，终是人千里，书启哪卷？才是我爱你的序言。
不管在那里，只要有君在的地方，臣妾都会幸福。
四叶草的每一片幸福，都为一个特定的人量身定做。
思念化作了一个个的字迹，化作了无声无语的讯息，飘向了你。这是无声的祝福：看信息的你天天有个好心情，别忘记回短信。
为什么人总是在接近幸福时倍感幸福，却在幸福进行时变得患得患失。
我，正如我的幸福里只有你。
爱而不伤别人的心，被爱而不内疚是最幸福的。
亲爱的，我很自私的独自拥有你的爱，我幸福。
对我来讲，最大的幸福，就是当我深夜应酬归来倒在沙发上时，你端给我一碗小米粥。
爱，伸出双手握不住，想你的夜晚没有你，只有，思念成灾一往情深的自己。就像一只孤独的大雁，扇动着疲惫的翅膀，望天也迷茫，望水也迷茫，春去了夏，夏走了秋，秋转来了冬，轮回中你依旧是我的唯一。
如果此生能够谈一段永不过期的恋爱，结一段永不结束的婚姻，这就是幸福。
岁月无声，一切都在疯长，没有什么可以完好无缺。
幸福是一段撼动灵魂的音乐。无论交响、协奏，还是仙音梵文；若与爱契合，就能与心共舞。豪情处且高歌，苦痛时且哭泣。
想你是一种幸福，眼中有爱，爱的那么深沉。
于世界而言，你是一个人；但是对于我，你是我的整个世界。
茫茫人海，你是我唯一不能放弃的挂念，也是我最无法放心的无法，无论你走到天涯海角，我都会祝愿你！
若说花事了，福知多少。
生活就是无数个烟火气息的小细节组成。其实也慢慢喜欢上这种生活，忙忙碌碌吵吵闹闹。是小幸福也是小幸运。
我爱你，犹如爱落日和月色：我想留住那些时刻，然而我想占有的，只是占有的感觉。——佩索阿
全世界，我只想和你嗨。
相爱是一门艺术，爱是两个人一起成长，这就必须得有交流，有交流才有了解，有了解才有更深的爱。
"""

    # 每日问候
    literature_all = str_all.split("\n")
    greetings_today = random.choice(literature_all)

    return weather, temp, tempn, now_weather, wind_direction, air_humidity, ultraviolet_rays, air_quality, pm, sunrise, sunset, greetings_today


##===================================================================================
def get_anniversary_day(anniversary, year, today):
    # 获取纪念日的对应月和日
    anniversary_month = int(anniversary.split("-")[1])
    anniversary_day = int(anniversary.split("-")[2])
    # 今年纪念日
    year_date = date(year, anniversary_month, anniversary_day)

    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today < year_date:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = date((year + 1), anniversary_month, anniversary_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]

    return birth_day


def get_birthday(birthday, year, today):
    birthday_year = birthday.split("-")[0]
    # 判断是否为农历生日
    if birthday_year[0] == "r":
        r_mouth = int(birthday.split("-")[1])
        r_day = int(birthday.split("-")[2])
        # 今年生日
        birthday = ZhDate(year, r_mouth, r_day).to_datetime().date()
        year_date = birthday


    else:
        # 获取国历生日的今年对应月和日
        birthday_month = int(birthday.split("-")[1])
        birthday_day = int(birthday.split("-")[2])
        # 今年生日
        year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        if birthday_year[0] == "r":
            # 获取农历明年生日的月和日
            r_last_birthday = ZhDate((year + 1), r_mouth, r_day).to_datetime().date()
            birth_date = date((year + 1), r_last_birthday.month, r_last_birthday.day)
        else:
            birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day


def get_ciba():
    url = "http://open.iciba.com/dsapi/"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = get(url, headers=headers)
    note_en = r.json()["content"]
    note_ch = r.json()["note"]
    return note_ch, note_en


def send_message(to_user, access_token, city_name, weather, max_temperature, min_temperature, note_ch, note_en,
                 now_weather, wind_direction, air_humidity, ultraviolet_rays, air_quality, pm, sunrise, sunset,
                 greetings_today):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 获取在一起的日子的日期格式
    love_year = int(config["love_date"].split("-")[0])
    love_month = int(config["love_date"].split("-")[1])
    love_day = int(config["love_date"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    
    
    # 获取相识的日子的日期格式
    love_year_1 = int(config["love_date_1"].split("-")[0])
    love_month_1 = int(config["love_date_1"].split("-")[1])
    love_day_1 = int(config["love_date_1"].split("-")[2])
    love_date_1 = date(love_year_1, love_month_1, love_day_1)
    # 获取相识的日期差
    love_days_1 = str(today.__sub__(love_date_1)).split(" ")[0]
    
    # 获取所有生日数据和纪念日数据
    birthdays = {}
    anniversary = {}
    for k, v in config.items():
        if k[0:8] == "birthday":
            birthdays[k] = v
        if k[0:10] == "anniversar":
            anniversary[k] = v
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week)
#                 "color": get_color()
            },
            "city": {
                "value": city_name
#                 "color": get_color()
            },
            "weather": {
                "value": weather
#                 "color": get_color()
            },
            "min_temperature": {
                "value": min_temperature
#                 "color": get_color()
            },
            "max_temperature": {
                "value": max_temperature
#                 "color": get_color()
            },
            "love_day_1": {
                "value": love_days_1
#                 "color": get_color()
            },
            "love_day": {
                "value": love_days
#                 "color": get_color()
            },
            "note_en": {
                "value": note_en
#                 "color": get_color()
            },
            "note_ch": {
                "value": note_ch
#                 "color": get_color()
            },
            "now_weather": {
                "value": now_weather
#                 "color": get_color()
            },
            "wind_direction": {
                "value": wind_direction
#                 "color": get_color()
            },
            "air_humidity": {
                "value": air_humidity
#                 "color": get_color()
            },
            "ultraviolet_rays": {
                "value": ultraviolet_rays
#                 "color": get_color()
            },
            "air_quality": {
                "value": air_quality
#                 "color": get_color()
            },
            "pm": {
                "value": pm
#                 "color": get_color()
            },
            "sunrise": {
                "value": sunrise
#                 "color": get_color()
            },
            "sunset": {
                "value": sunset
#                 "color": get_color()
            },
            "greetings_today": {
                "value": greetings_today
#                 "color": get_color()
            }
        }
    }
    for key, value in birthdays.items():
        # 获取距离下次生日的时间
        birth_day = get_birthday(value["birthday"], year, today)
        if birth_day == 0:
            birthday_data = "今天{}生日哦，祝{}生日快乐！".format(value["name"], value["name"])
        else:
            birthday_data = "{}的生日还有{}天".format(value["name"], birth_day)
        # 将生日数据插入data
        data["data"][key] = {"value": birthday_data}
        
        
    for key, value in anniversary.items():
        anniversary_day = get_anniversary_day(value["anniversary"], year, today)
        if anniversary_day == 0:
            anniversary_data = "一切不尽言语中，要抱起宝贝转圈圈~要把宝贝亲的晕过去~"
        else:
            anniversary_data = "和宝贝贴贴还有{}天".format(anniversary_day)
        # 将纪念日插入data
        data["data"][key] = {"value": anniversary_data}
        
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)


if __name__ == "__main__":
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)

# 获取accessToken
accessToken = get_access_token()
# 接收的用户
users = config["user"]
# 传入省份和市获取天气信息
province, city = config["province"], config["city"]
weather, max_temperature, min_temperature, now_weather, wind_direction, air_humidity, ultraviolet_rays, air_quality, pm, sunrise, sunset, greetings_today = get_weather(
    province, city)

# 获取词霸每日金句
note_ch, note_en = get_ciba()
# 公众号推送消息
for user in users:
    send_message(user, accessToken, city, weather, max_temperature, min_temperature, note_ch, note_en, now_weather,
                 wind_direction, air_humidity, ultraviolet_rays, air_quality, pm, sunrise, sunset, greetings_today)
os.system("pause")
