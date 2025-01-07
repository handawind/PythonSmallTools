import paramiko, json, os
from pathlib import Path

def get_server_serial_number(host, username='root', password=""):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command('dmidecode -s system-serial-number')
        serial_number = stdout.read().decode('utf-8').strip()
        ssh.close()
        return serial_number
    except Exception as e:
        print(f"Error connecting to {host}: {e}")
        return None


def serial_number_host_add(servers, server_in):
    servers.append(server_in)
    print(servers)
    with open(server_list_path, 'w', encoding='utf-8') as file:
        contents = servers
        server_list_path.write_text(json.dumps(contents, ensure_ascii=False), encoding='utf-8')
    return servers


def command_send_in(servers):
    for server in servers:
        serial_number = get_server_serial_number(server)
        if serial_number:
            # print(f"Server {server} Serial Number: {serial_number}")
            print(f"{serial_number}")


if __name__ == "__main__":
    server_list_path = Path('./files/服务器序列号.json')
    servers = []
    if server_list_path.exists():
        choose = input('文件已存在，删除还是继续？ rm 删除，con 继续\n输入选择：')
        if choose == 'rm':
            os.remove(server_list_path)
            while True:
                server_in = input('请输入IP地址，如果已完成输入，请输入yes或y，如果退出请输入quit\n输入：')
                if server_in == 'yes':
                    command_send_in(servers)
                elif server_in == 'quit':
                    break
                else:
                    serial_number_host_add(servers, server_in)

        elif choose == 'con':
            with open(server_list_path, 'r', encoding='utf-8') as file:
                servers = json.loads(server_list_path.read_text())
            print(servers)
            while True:
                server_in = input('请输入IP地址，如果已完成输入，请输入yes或y，如果退出请输入quit\n输入：')
                if server_in == 'yes':
                    command_send_in(servers)
                elif server_in == 'quit':
                    break
                else:
                    serial_number_host_add(servers, server_in)
    else:
        while True:
            server_in = input('请输入IP地址，如果已完成输入，请输入yes或y，如果退出请输入quit\n输入：')
            if server_in == 'yes':
                command_send_in(servers)
            elif server_in == 'quit':
                break
            else:
                serial_number_host_add(servers, server_in)
