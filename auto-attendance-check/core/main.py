import fire

class Commands(object):
    """
    auto-attendance-checkのAPI
    sshでCLI実行する目的

    Note
    ----
    GUIの操作に対応させて必要なコマンドを作っていく
    """
    def AttendData():
        pass

    def TekePhoto():
        pass

    def SetTimeTable():
        pass

    def Configuration():
        pass


if __name__ == "__main__":
    fire.Fire(Commands)
