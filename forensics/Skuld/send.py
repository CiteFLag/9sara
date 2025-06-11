import requests
target_webhook = "https://discord.com/api/webhooks/1379764968018415646/uVTgeH2cx8bXlnbPC1J03qpqI3nxCB0D74py8GemtqtJLEsfneoPRY9nqMngk6_vAGd9"
payload = {
    "content": f"!invite https://discord.com/api/webhooks/****/****"
}
response = requests.post(target_webhook, json=payload)
if response.status_code == 204:
    print("Message sent successfully!")
else:
    print(f"Failed to send message: {response.status_code}\n{response.text}")
