def get_time_diff_str(sec: float or int):
    assert sec >= 0
    assert sec < 60 * 60, str(sec)
    # 60秒未満
    if sec // 60 == 0:
        return "{}sec".format(str(int(sec)))
    # 60分未満
    if sec // int(60 * 60) == 0:
        return "{}min{}sec".format(str(int(sec // 60)), str(int(sec % 60)))

