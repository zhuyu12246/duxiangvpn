# 自己搭建专属回国独享vpn或者海外vpn 使用WireGuard

**安装前请确认**
需要有能够访问公网的服务器，或者能访问公网服务器的VPS。同时要确认是否有ipv4和ipv6
以回国为例子：
如果只有其中一个可以对网页进行回国访问，可以访问到该地区未有权限的视频

如果都有 则可以全局代理，steam上面国区的游戏可以在海外进行下载游玩

**云服务器 本目录使用腾讯云 OpenCloudOS**
UDP 51820（WireGuard 默认端口）放行

协议：UDP
端口：51820
来源：0.0.0.0/0

**安装 WireGuard**

更新系统

```
sudo dnf update -y
```

安装 WireGuard

```
sudo dnf install wireguard-tools -y
```

安装 iptables（用于 NAT 转发）

```
sudo dnf install iptables -y
```

**生成密钥**

服务器密钥

```
wg genkey | tee server.key | wg pubkey > server.pub
```

客户端密钥

```
wg genkey | tee client.key | wg pubkey > client.pub
```

**服务器端配置**
/etc/wireguard/wg0.conf

```
[Interface]
PrivateKey = <服务器私钥>
Address = 10.0.0.1/24, fd10:8888::1/64[ipv6]
ListenPort = 51820

PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE; ip6tables -A FORWARD -i wg0 -j ACCEPT; ip6tables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE; ip6tables -D FORWARD -i wg0 -j ACCEPT; ip6tables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
PublicKey = <客户端公钥>
AllowedIPs = 10.0.0.2/32, fd10:8888::2/128
```

`eth0` 改成服务器真实网卡名：`ip a` 查看。

**开启内核转发**

```
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
echo "net.ipv6.conf.all.forwarding=1" | sudo tee -a /etc/sysctl.conf
echo "net.ipv6.conf.default.forwarding=1" | sudo tee -a /etc/sysctl.conf

sudo sysctl -p

```

 /etc/sysctl.conf里面的这两个配置必须删掉

net.ipv6.conf.all.disable_ipv6=1
net.ipv6.conf.default.disable_ipv6=1

开启 NAT 转发 重要这是全局的关键 ipv4和ipv6都进行改变，实现全局

```
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

**启动 WireGuard**

```
sudo wg-quick up wg0
```

输入wg 有输出表示成功

**客户端配置**

注意客户端也要下载WireGuard,可用代码自动检测下载删除等

```
[Interface]
PrivateKey = <客户端私钥>
Address = 10.0.0.2/24, fd10:8888::2/64[ipv6地址]
DNS = 8.8.8.8

[Peer]
PublicKey = <服务器公钥>
Endpoint = <服务器公网IP>:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```

**python文件打包**
给windows使用

```
pyinstaller --onefile --uac-admin vpn_tool.py
```

windos的代码需要自行修改，本目录只用于mac
或者安装windows的WireGuard，把wg-client.conf文件拖入那个软件里面就行了
