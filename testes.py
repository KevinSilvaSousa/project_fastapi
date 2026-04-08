import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjQsImV4cCI6MTc3NTY3MjUxNX0.vAIviuGv0N8I9zB540XcW4uImUVWJ-Uz5Ehnbt6ovY4"
}
requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)

print(requisicao)
print(requisicao.json())