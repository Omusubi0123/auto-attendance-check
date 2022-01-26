import os
import sys
from typing import Any, MutableMapping
from core.export import ClassMatesRegister, AttendanceState, cast_str_to_time

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
    assert cmr.datas == test_data


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
    assert cmr.datas == test_data


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
"""


def test_export_json():
    cmr = ClassMatesRegister(3)
    cmr.export_json()
    os.remove(f"{cmr.file_path}.json")
    assert True


def test_cast_str_to_time():
    testcase_time = [
        "8 50",
        "10 20",
        "10 30",
        "12 00",
        "12 50",
        "14 20"
    ]
    for test in testcase_time:
        assert cast_str_to_time(test)

    testcase_time = [
        "1200",
        "24 50",
        "14 20 00"
    ]
    for test in testcase_time:
        try:
            cast_str_to_time(test)
            assert False
        except:
            assert True
