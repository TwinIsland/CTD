import time


def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def fail_msg(msg, sId="ADMIN"):
    c = "[X] sId: " + str(sId) + " --- " + msg + "    " + get_time() + "\n"
    file = open("EVENT.TXT", 'a+')
    file.write(c)
    file.close()
    return c


def ok_msg(msg, sId="ADMIN"):
    c = "[V] sId: " + str(sId) + " --- " + msg + "    " + get_time() + "\n"
    file = open("EVENT.TXT", 'a+')
    file.write(c)
    file.close()
    return c


def rec_msg(msg, sId="ADMIN"):
    c = "[-] sId: " + str(sId) + " --- " + msg + "    " + get_time() + "\n"
    file = open("EVENT.TXT", 'a+')
    file.write(c)
    file.close()
    return c
