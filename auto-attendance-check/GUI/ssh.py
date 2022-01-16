# connecting ssh

import paramiko
from tkinter import messagebox


def connect_SSH(IP_ADDRESS: str, USER_NAME: str, PASSWORD: str, CMD: str):
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

    try:
        client.connect(IP_ADDRESS, username=USER_NAME, password=PASSWORD, timeout=3.9)
    except Exception:
        messagebox.showerror("エラー", "ラズパイに接続できませんでした")
        return

    # コマンド呼び出し
    stdin, stdout, stderr = client.exec_command(CMD)

    client.close()

    del client, stdin, stdout, stderr
