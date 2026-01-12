class CommandsAPI:
    def __init__(self, client):
        self.client = client

    def create_command(self, device_id, command):
        return self.client.create_command(device_id, command)
    
    def get_command_status(self, command_id):
        return self.client.get_command_status(command_id)
    
    def wait_polling(self, command_id, timeout=30):
        return self.client.wait_polling(command_id, timeout=30)