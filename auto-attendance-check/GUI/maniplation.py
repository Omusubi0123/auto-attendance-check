#GUI sub file

#ボタンクリック時の操作
class Maniplation():
    def RefAttendData():
        """
        「出席状況」button was pushed

        Notes
        powershellを開き、出席データを格納している機器へアクセス
        
        """
        pass

    def TakePhotoCom():
        """
        「教室撮影」button was pushed
        
        Notes
        powershellを開き、ラズパイにSSH接続
        →ラズパイへ撮影を命令　撮影した教室の画像を画像処理部の画像フォルダに格納する
        →撮影した画像はPC側にも送信　GUI操作者による確認を可能に
        →ラズパイへ画像解析を命令
        →ラズパイとのSSH接続を終了
        """
        pass

    def SetTimetable():
        """
        「時間割」button was pushed
        """
        pass

    def Configuration():
        """
        「設定」button was pushed
        Notes
        """
        pass

