import sys
from core.mail import check_mailaddres

sys.path.append("../../..")


def test_check_mailaddress():
    pass_case = [
        "a12345@gunma.kosen-ac.jp",
        "a12345@outlook.com",
        "a-123.456@gmail.com",
    ]

    for case in pass_case:
        try:
            check_mailaddres(case)
            assert True
        except ValueError:
            assert False

    error_case = [
        "a-12345",
        " a12345@outlook.com",
    ]

    for case in error_case:
        try:
            check_mailaddres(case)
            assert False
        except ValueError:
            assert True

    assert True
