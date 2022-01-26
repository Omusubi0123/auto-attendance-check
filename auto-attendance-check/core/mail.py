"""
欠席連絡のメールを送信するためのモジュール
"""

import re
import datetime
import smtplib
from email import message

import toml


def send_mail(to: str) -> None:
    """
    欠席判定された人に欠席確認のメールを送信する

    Parameters
    ----------
    to : str
    送信先のメールアドレス

    Raises
    ------
    ValueError
        値がメールアドレスとして正しくない

    Note
    ----
    メール送信者の情報は`mail_secret.toml`に保存する
    以下のように送信者のメールアドレス・メールサーバーログイン用のパスワードを記入する
    ```toml
    [sender]
    address = "xxxxx@example.com"
    password = "xxxxx"
    ```

    See Also
    --------
    check_mailaddress()
    """
    check_mailaddres(to)

    mail_sender = toml.load(open("auto-attendance-check/core/mail_secret.toml"))

    smtp_host = "smtp.live.com"
    smtp_port = 587
    to_mail = to
    from_mail = mail_sender["sender"]["address"]
    username = mail_sender["sender"]["address"]
    password = mail_sender["sender"]["password"]
    subject = "[自動出欠確認プログラム] 欠席確認"
    content = f"""
    {to}様、

    自動出欠確認プログラムです。

    {datetime.datetime.now().strftime(r"%m月%d日 %H:%M")}の出欠確認で、欠席判定されました。
    もし、誤判定の場合は連絡お願いします。
    """

    msg = message.EmailMessage()
    msg.set_content(content)
    msg["Subject"] = subject
    msg["From"] = from_mail
    msg["To"] = to_mail

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.send_message(msg)
    server.quit()


def check_mailaddres(to: str) -> None:
    """
    正規表現によってメールアドレスとして有効かどうか最低限のチェックを行う

    Parameters
    ----------
    to : str
    送信先のメールアドレス

    Raises
    ----
    ValueError
        値がメールアドレスとして正しくない
    """
    mail_pattarn = r"^[a-zA-Z0-9_+-]+(.[a-zA-Z0-9_+-]+)*@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$"
    if re.match(pattern=mail_pattarn, string=to) is None:
        raise ValueError("メールアドレスの値が正しくありません")
