import subprocess
import sys
import os

# 客户端配置文件路径
# WG_CONFIG_PATH = os.path.expanduser("~/wg-client.conf")
WG_CONFIG_PATH = os.path.expanduser("./wg-client.conf")
VPN_NAME = "wg0"  # 配置文件里 [Interface] 的名字

def connect_vpn():
    print("正在连接 VPN...")
    try:
        subprocess.run(["sudo", "wg-quick", "up", WG_CONFIG_PATH], check=True)
        print("VPN 已连接 ✅")
    except subprocess.CalledProcessError:
        print("连接失败 ❌")

def disconnect_vpn():
    print("正在断开 VPN...")
    try:
        subprocess.run(["sudo", "wg-quick", "down", WG_CONFIG_PATH], check=True)
        print("VPN 已断开 ✅")
    except subprocess.CalledProcessError:
        print("断开失败 ❌")

def status_vpn():
    print("VPN 状态：")
    subprocess.run(["wg"])

def main():
    while True:
        print("\n=== VPN 控制菜单 ===")
        print("1. 连接 VPN")
        print("2. 断开 VPN")
        print("3. 查看 VPN 状态")
        print("4. 退出")
        choice = input("请选择操作 (1-4): ").strip()

        if choice == "1":
            connect_vpn()
        elif choice == "2":
            disconnect_vpn()
        elif choice == "3":
            status_vpn()
        elif choice == "4":
            print("退出程序")
            sys.exit()
        else:
            print("无效选项，请重新选择")

if __name__ == "__main__":
    main()