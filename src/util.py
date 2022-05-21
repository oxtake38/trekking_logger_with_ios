def get_time_diff_str(sec):
    assert sec < 60 * 60, str(sec)
    # 60秒未満
    if sec // 60 == 0:
        return "{}sec".format(str(int(sec)))
    # 60分未満
    if sec // int(60 * 60) == 0:
        return "{}min{}sec".format(str(int(sec // 60)), str(int(sec % 60)))


def t():
    return 4