import os
import json


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


while True:
    print("=================================================")
    print("Hello, which of these do you want to do?")
    q1 = input(
        "Add Proxy-1 / Submit Bot Information-2 / See Bot Information-3 / Exit-4 (1/2/3/4): "
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

    else:
        print("Invalid input! Please select a valid option.")
