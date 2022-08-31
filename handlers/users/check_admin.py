import config


def check_admin(user_id):
    res = False
    for admin in config.ADMINS:
        if user_id == int(admin):
            res = True
    return res
