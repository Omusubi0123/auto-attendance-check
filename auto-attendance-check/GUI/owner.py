# 「設定」クラス

import toml


class Owner:
    """
    「個人用設定」情報をまとめたクラス
    """

    def __init__(self):
        with open("confirmation.toml", "rt") as fp:
            data = toml.load(fp)

        self.username = data["username"]
        self.schoolname = data["schoolname"]
        self.classname = data["classname"]
        self.interval = int(data["interval"])

    def update(
        self,
        username: str = "",
        schoolname: str = "",
        classname: str = "",
        interval: int = -1,
    ):
        if username != "":
            self.username = username

        if schoolname != "":
            self.schoolname = schoolname

        if classname != "":
            self.classname = classname

        if interval >= 0:
            self.interval = interval

        enter_toml = {
            "username": self.username,
            "schoolname": self.schoolname,
            "classname": self.classname,
            "interval": self.interval,
        }
        toml.dump(enter_toml, open("confirmation.toml", mode="w"))
