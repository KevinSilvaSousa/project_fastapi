import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjksImV4cCI6MTc3NjAxOTcxOX0.Wf7Xx0GKuL1q8BnGY1giDFpih3vGGbUA_WUUvrYZl-I"
}
requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)

print(requisicao)
print(requisicao.json())