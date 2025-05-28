import httpx

headers = {"Content-Type": "application/x-www-form-urlencoded"}
params = {'key': '',}  #接口申请地址:https://www.juhe.cn/docs/api/id/95
url = "http://v.juhe.cn/joke/randJoke"
r = httpx.get(url, headers=headers, params=params)
data = r.json()
print(data)