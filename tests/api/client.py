import requests
import time

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    # Создание команды
    def create_command(self, device_id, command):
        url = f"{self.base_url}/api/commands"
        payload = {"device_id": device_id, "command": command}

        print(f"Creating command for device: {device_id}, command: {command}")

        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()

        print(f"Command created - ID: {result['id']}, Status: {result['status']}")

        return result

    # Получение статуса
    def get_command_status(self, command_id):
        url = f"{self.base_url}/api/commands/{command_id}"

        print(f"Getting status for command: {command_id}")

        response = requests.get(url)

        print(f"Status response: {response.status_code}")

        response.raise_for_status()
        result = response.json()
            
        print(f"Command {command_id} status: {result['status']}")

        return result

    # Ассинхронность, polling, таймаут
    def wait_polling(self, command_id, timeout=30):
        print(f"Starting polling for command {command_id}, timeout: {timeout}s")
        end_time = time.time() + timeout
        poll_count = 0
            
        while time.time() < end_time:
            poll_count += 1

            try:
                print(f"Request #{poll_count} for command {command_id}")
                status_data = self.get_command_status(command_id)
                current_status = status_data['status']

                print(f"Current status: {current_status}")
                if current_status in ['SUCCESS', 'FAILED']:
                    print(f"Command completed with status: {current_status}")
                    return status_data
                    
                print(f"Waiting 1 second...")
                time.sleep(1)

            except requests.HTTPError as err:
                # Обработка временных ошибок сервера (5xx)
                if err.response.status_code >= 500:
                    print(f"Temporary server error ({err.response.status_code}). Retrying in 1 second...")
                    time.sleep(1)
                    continue
                else:
                    # 4xx ошибки (клиентские)
                    print(f"Client error: {err.response.status_code}")
                    raise
    
        # Таймаут
        print(f"Timeout! Command {command_id} did not complete in {timeout} seconds")
        raise TimeoutError(f"Command {command_id} did not complete in {timeout} seconds")