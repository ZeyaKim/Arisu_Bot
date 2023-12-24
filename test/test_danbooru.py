import requests

url = "https://danbooru.donmai.us/posts.json"
params = {
    "search": {
    },
    "limit": 200
}

response = requests.get(url, params=params)

if response.status_code == 200:
    posts = response.json()
    scores = [post['score'] for post in posts]
    print("최고 점수:", max(scores), "url", posts[scores.index(max(scores))]['file_url'])
else:
    print("요청 실패:", response.status_code)
