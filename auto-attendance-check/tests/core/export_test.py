import sys
import os
from core.export import ClassMatesRegister, AttendanceState

sys.path.append("../../..")


def test_init():
    cmr = ClassMatesRegister(1)
    test_data = [
        {
            "student number": 1,
            "name": "",
            "attendance states": [AttendanceState.NONE.value],
        }
    ]
    assert cmr.data == test_data


def test_insert():
    cmr = ClassMatesRegister(3)
    new_data = [AttendanceState.ATTEND, AttendanceState.ATTEND, AttendanceState.ATTEND]
    cmr.insert_data(new_data)
    test_data = [
        {
            "student number": 1,
            "name": "",
            "attendance states": [
                AttendanceState.NONE.value,
                AttendanceState.ATTEND.value,
            ],
        },
        {
            "student number": 2,
            "name": "",
            "attendance states": [
                AttendanceState.NONE.value,
                AttendanceState.ATTEND.value,
            ],
        },
        {
            "student number": 3,
            "name": "",
            "attendance states": [
                AttendanceState.NONE.value,
                AttendanceState.ATTEND.value,
            ],
        },
    ]
    assert cmr.data == test_data


"""
まだ動かないテスト
あとでちゃんと書く

def test_export_csv():
    cmr = ClassMatesRegister(3)
    cmr.exprot_csv()
    os.remove(f"{cmr.file_path}.csv")


def test_export_excel_csv():
    cmr = ClassMatesRegister(3)
    cmr.export_excel_csv()
    os.remove(f"{cmr.file_path}.csv")


def test_export_json():
    cmr = ClassMatesRegister(3)
    cmr.export_json()
    os.remove(f"{cmr.file_path}.json")
"""
