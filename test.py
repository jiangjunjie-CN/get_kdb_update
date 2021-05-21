import datetime
import os
print(type(datetime.datetime.today().year))
print(type(datetime.datetime.today().month))


def check_dir():
    year = str(datetime.datetime.today().year)
    month = str(datetime.datetime.today().month) + '月'
    updateRoot = os.path.join(os.getcwd(), 'update_history', year)
    updateFile = os.path.join(updateRoot, '{}.xlsx'.format(month))
    if not os.path.exists(updateRoot):
        os.mkdir(updateRoot)
    if not os.path.exists(updateFile):
        updateFile = None
    return (updateRoot, updateFile)


check_dir()