# connecting ssh

import paramiko


def connect_SSH(IP_ADDRESS, USER_NAME, PASSWORD, CMD):
    """
    指定機器へSSH接続する

    Parameters
    ----------
    IP_ADDRESS : str
        接続機器のipアドレス

    USER_NAME : str
        接続機器のusername

    PASSWORD : str
        接続機器のパスワード

    CMD : str list
        実行命令をまとめたリスト
    """

    # SSH接続
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(IP_ADDRESS, username=USER_NAME, password=PASSWORD)

    # コマンド呼び出し
    stdin, stdout, stderr = client.exec_command(CMD)

    client.close()
    del client, stdin, stdout, stderr
