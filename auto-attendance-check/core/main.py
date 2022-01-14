import fire


class Commands(object):
    """
    auto-attendance-checkのAPI
    sshでCLI実行する目的

    Note
    ----
    GUIの操作に対応させて必要なコマンドを作っていく
    """

    def attend_data():
        """
        ?
        """
        pass

    def teke_photo():
        """
        写真を撮影
        """
        pass

    def set_time_table():
        """
        時間割の設定
        """
        pass

    def configuration():
        """
        ?
        """
        pass


def main():
    fire.Fire(Commands)
