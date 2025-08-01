import os
import json
import time
import requests
from pyrogram import Client


def test_proxies_and_get_client(session_name="proxy_session"):
    proxies_file = os.path.join(os.path.dirname(__file__), "proxies.json")
    bot_info_file = os.path.join(os.path.dirname(__file__), "BotInfo.json")

    if not os.path.exists(proxies_file) or not os.path.exists(bot_info_file):
        return None

    with open(bot_info_file, "r") as f:
        bot_info = json.load(f)

    api_id = bot_info.get("api_id")
    api_hash = bot_info.get("api_hash")
    bot_token = bot_info.get("token")

    if not all([api_id, api_hash, bot_token]):
        return None

    with open(proxies_file, "r") as f:
        proxies = json.load(f)
        if not proxies or not isinstance(proxies, list):
            return None

    def test_proxy_speed(proxy):
        try:
            test_url = "https://core.telegram.org"
            proxy_url = f"http://{proxy['hostName']}:{proxy['port']}"
            test_proxies = {
                "http": proxy_url,
                "https": proxy_url,
            }
            start = time.time()
            response = requests.get(test_url, proxies=test_proxies, timeout=5)
            if response.status_code == 200:
                return time.time() - start
            else:
                return float("inf")
        except:
            return float("inf")

    best_proxy = None
    best_time = float("inf")

    for proxy in proxies:
        duration = test_proxy_speed(proxy)
        print(f"🔎 Proxy {proxy['hostName']}:{proxy['port']} → {duration:.2f} sec")
        if duration < best_time:
            best_time = duration
            best_proxy = proxy

    if not best_proxy:
        print("❌ No working proxy found.")
        return None

    print(
        f"✅ Best Proxy: {best_proxy['hostName']}:{best_proxy['port']} in {best_time:.2f}s"
    )

    client = Client(
        session_name,
        api_id=api_id,
        api_hash=api_hash,
        bot_token=bot_token,
        proxy={
            "scheme": "mtproto",
            "hostname": best_proxy["hostName"],
            "port": best_proxy["port"],
            "secret": best_proxy["secret"],
        },
    )

    return client


def addProxy(hostName, port, secret):
    try:
        if not all([hostName, port, secret]):
            raise ValueError("All proxy parameters are required")

        try:
            port = int(port)
        except ValueError:
            raise ValueError("Port must be a valid number")

        proxy_data = {
            "hostName": hostName.strip(),
            "port": port,
            "secret": secret.strip(),
        }

        file_path = os.path.join(os.path.dirname(__file__), "proxies.json")

        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)
            current_data = []
        else:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    current_data = json.load(f)
                    if not isinstance(current_data, list):
                        current_data = []
            except (json.JSONDecodeError, ValueError):
                current_data = []

        current_data.append(proxy_data)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(current_data, f, ensure_ascii=False, indent=4)

        print(f"✅ Proxy {hostName}:{port} added successfully.")
        return True

    except Exception as e:
        print(f"❌ Failed to add proxy: {str(e)}")
        return False


def addProxiesFromList():
    urls_file = os.path.join(os.path.dirname(__file__), "proxy_links.txt")
    if not os.path.exists(urls_file):
        print("File 'proxy_links.txt' not found!")
        return

    with open(urls_file, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    added = 0
    for url in lines:
        if not url.startswith("https://t.me/proxy?"):
            continue

        try:
            query = url.split("?")[1]
            params = dict(param.split("=") for param in query.split("&"))
            host = params.get("server")
            port = params.get("port")
            secret = params.get("secret")
            if addProxy(host, port, secret):
                added += 1
        except Exception as e:
            print(f"Skipping invalid proxy link: {url}")

    print(f"✅ Added {added} proxies from list.")


def subBotInfo(token, api_id, api_hash):
    file_path = os.path.join(os.path.dirname(__file__), "BotInfo.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(
            {"token": token, "api_id": api_id, "api_hash": api_hash},
            f,
            ensure_ascii=False,
            indent=4,
        )


def showBotInfo():
    file_path = os.path.join(os.path.dirname(__file__), "BotInfo.json")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            deserialized_data = json.load(f)
            print("Bot Information:")
            print(
                f'Bot Token: {deserialized_data["token"]}\nBot Api_Id: {deserialized_data["api_id"]}\nBot Api_Hash: {deserialized_data["api_hash"]}'
            )

    except FileNotFoundError:
        print("Error: BotInfo.json file not found!")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in BotInfo.json!")


def testProxiesAndClear(session_name="proxy_session"):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    proxies_file = os.path.join(BASE_DIR, "proxies.json")
    bot_info_file = os.path.join(BASE_DIR, "BotInfo.json")

    if not os.path.exists(proxies_file) or not os.path.exists(bot_info_file):
        print("❌ Required files not found.")
        return None

    with open(bot_info_file, "r") as f:
        bot_info = json.load(f)

    api_id = bot_info.get("api_id")
    api_hash = bot_info.get("api_hash")
    bot_token = bot_info.get("token")

    if not all([api_id, api_hash, bot_token]):
        print("❌ Bot info is incomplete.")
        return None

    with open(proxies_file, "r") as f:
        proxies = json.load(f)

    if not proxies or not isinstance(proxies, list):
        print("❌ proxies.json is empty or invalid.")
        return None

    def test_proxy(proxy):
        try:
            test_url = "https://core.telegram.org"
            proxy_url = f"http://{proxy['hostName']}:{proxy['port']}"
            proxy_dict = {
                "http": proxy_url,
                "https": proxy_url,
            }
            start = time.time()
            response = requests.get(test_url, proxies=proxy_dict, timeout=6)
            if response.status_code == 200:
                return time.time() - start
            return float("inf")
        except:
            return float("inf")

    valid_proxies = []
    print("\n🔍 Testing all proxies...\n")

    for proxy in proxies:
        duration = test_proxy(proxy)
        if duration < float("inf"):
            print(f"✅ {proxy['hostName']}:{proxy['port']} → {duration:.2f} sec")
            valid_proxies.append(proxy)
        else:
            print(f"❌ {proxy['hostName']}:{proxy['port']} → Connection failed")

    with open(proxies_file, "w", encoding="utf-8") as f:
        json.dump(valid_proxies, f, ensure_ascii=False, indent=4)

    print(f"\n🧹 {len(valid_proxies)} working proxies saved.")
    print("✅ Cleanup and saving completed successfully.\n")


while True:
    print("=================================================")
    print("Hello, which of these do you want to do?")
    q1 = input(
        "Add Proxy-1 / Submit Bot Information-2 / See Bot Information-3 / Exit-4 / Add from List-5 / Clear Proxies-6 (1/2/3/4/5/6): "
    )

    if q1 == "1":
        print("=================================================")
        hostName = input("Write the 'HostName': ")
        port = input("Write the 'Port': ")
        secret = input("Write the 'Secret': ")

        if not all([hostName, port, secret]):
            print("All fields are required!")
        else:
            addProxy(hostName=hostName, port=port, secret=secret)

    elif q1 == "2":
        print("=================================================")
        token = input("Write the 'Bot Token': ")
        api_id = input("Write the 'Bot Api_Id': ")
        api_hash = input("Write the 'Bot Api_Hash': ")

        subBotInfo(token=token, api_id=api_id, api_hash=api_hash)

    elif q1 == "3":
        print("=================================================")
        showBotInfo()

    elif q1 == "4":
        print("Exiting program...")
        break

    elif q1 == "5":
        print("=================================================")
        addProxiesFromList()
    elif q1 == "6":
        print("=================================================")
        testProxiesAndClear()

    else:
        print("Invalid input! Please select a valid option.")
