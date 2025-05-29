"""
使用playwright爬取微博评论，并清洗冗余数据，保存为CSV
"""
from playwright.sync_api import sync_playwright
import random
import pandas as pd
import time
start_time=time.time()
# 从浏览器复制的 Cookie 字符串
cookie = """
SCF=AqGecu92L8Kax9sGtV4bPR3b5Ug2bkbCwvt9JfV41Se8jRwHwWJqUDXvHBmmZRxPGw0mBF1dz3Q-AC0WDzm5cXk.; SUB=_2A25FM3cYDeRhGe5O61MQ9ifNyjuIHXVmMfbQrDV8PUNbmtANLRSkkW9NddxjB2U8rl9MOa0-cqQwrzdSuTmh2elW; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhH63ShEJ0rzMIS9iZIFVzZ5NHD95QReh5peKq4eK2NWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zN1h57eK2c1K2pS7tt; ALF=02_1751028808; SINAGLOBAL=7902481796954.946.1748436812735; UOR=,,cn.bing.com; _s_tentry=www.weibo.com; Apache=7967468910659.658.1748509042690; ULV=1748509042804:3:3:3:7967468910659.658.1748509042690:1748492364681; WBPSESS=IlMdLN47QY3a5Os0DivMXkY2jsvg4qINuW1G42iEo1G_lE6NgK24pbpG_V3VVobEETH0a3rGs2NI7B-qDisNQOeAyb7uGvkrb_wXiH1hr_toDaoQCzVHumq11meYL55IdtLjw9N5NyCWCsx0Ix_0gg==
"""

# 第0步 定义清洗数据函数--清洗字符列表->保存为csv
def drop_duplicate_data(context_list,subject=['评论','时间']):
    df=pd.DataFrame(context_list)
    df = df.drop_duplicates(subset=subject,keep='first')
    print(df)
    print(f'有用数据个数:{len(df)}')
    return df.to_csv('DATA/comments.csv')


# 第一步 解析 cookie 字符串为列表的函数--GPT提供
def parse_cookie(cookie_string):
    return [
        {
            'name': item.strip().split('=')[0],
            'value': item.strip().split('=', 1)[1],
            'domain': '.weibo.com',
            'path': '/',
        }
        for item in cookie_string.split(';') if '=' in item
    ]


with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    context = browser.new_context()

    # 第二步 设置 cookie
    context.add_cookies(parse_cookie(cookie))

    # 第三步 访问微博页面
    page = context.new_page()
    page.goto('https://weibo.com/6169991913/Pt7VwbdaJ#comment')

    print("✅ 页面加载成功")

    # 第四步 开始爬取数据

    # 定义总字典列表
    context_list = []

    prev_height=0
    # 第五步 鼠标滚轮向下
    while True:


        # 第七步 设置随机滚动像素和等待时间，模仿人类行为
        scroll_distance=random.randint(900,1100)
        waiting_time=random.randint(3000,3800)

        # 第八步 设置垂直滚动距离
        page.mouse.wheel(0, scroll_distance)

        # 第九步 设置等待时间
        page.wait_for_timeout(waiting_time)

        # 第十步 用高度控制程序结束
        curr_height = page.evaluate("document.documentElement.scrollHeight")

        # 如果当前页面高度和上一次一样就结束
        if curr_height == prev_height:
            break

        # 更新高度
        prev_height=curr_height

        # 第十一步 测试一-- 定位评论位置+保存

        # 定位时间地点
        pubtimes=page.locator('//div[@class="info woo-box-flex woo-box-alignCenter woo-box-justifyBetween"]/div[1]').all_text_contents()

        # 定位评论
        comment_elements = page.locator('//div[@class="vue-recycle-scroller__item-wrapper"]//div[@class="text"]/span').all_text_contents()

        length=len(comment_elements)
        for i in range(length):
            current_dict = {}

            # 处理特殊符号
            if not comment_elements[i]:
                continue

            current_dict['评论'] = comment_elements[i]
            current_dict['时间'] =pubtimes[i]
            # 保存
            context_list.append(current_dict)

    # 第十二步 检测打印列表
    print(context_list)
    print(f'原始数据个数:{len(context_list)}')

    # 第十三步 存储
    drop_duplicate_data(context_list)

    browser.close()

# 计时
end_time=time.time()
print(f'耗时:{end_time-start_time}')

















