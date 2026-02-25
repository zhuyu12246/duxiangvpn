import requests

# 测试 IPv4
r = requests.get("https://ipv4.icanhazip.com")
print("当前公网 IPv4:", r.text.strip())

# 测试 IPv6（可选）
r6 = requests.get("https://ipv6.icanhazip.com")
print("当前公网 IPv6:", r6.text.strip())
