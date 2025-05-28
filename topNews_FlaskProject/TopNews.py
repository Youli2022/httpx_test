import httpx

headers = {"Content-Type": "application/x-www-form-urlencoded"}
params = {'key': 'e5a68b164643f418b90fcc1ac2a2d5c1', 'page_size': '1'}  ##接口申请地址https://www.juhe.cn/docs/api/id/235
url = "http://v.juhe.cn/toutiao/index"
r = httpx.get(url, headers=headers, params=params)
data = r.json()
print(data)

if data.get('error_code') == 0 and data.get('result', {}).get('stat') == '1':
    news_list = data['result']['data']

    print(f"共获取 {len(news_list)} 条新闻：\n")

    for i, news in enumerate(news_list, 1):
        print(f"{i}. {news['title']}")
        print(f"   时间: {news['date']}")
        print(f"   来源: {news['author_name']}")
        print(f"   分类: {news['category']}")

        # 如果有缩略图则显示第一张
        if news.get('thumbnail_pic_s'):
            print(f"   缩略图: {news['thumbnail_pic_s']}")

        print(f"   详情链接: {news['url']}\n")

else:
    print(f"请求失败: {data.get('reason', '未知错误')}")
