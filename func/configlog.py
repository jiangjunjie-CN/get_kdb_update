import os
import logging
import logging.config


def config_log(logger_name):
    cur_dir = os.path.split(os.path.abspath(__file__))[0]
    log_conf_file = os.path.join(cur_dir, '../config/log.conf')
    log_file = os.path.join(cur_dir, 'log')
    if not os.path.exists(log_file):
        os.mkdir(log_file)
    if not os.path.exists(log_conf_file):
        err_msg = '日志配置文件{log_conf_file}不存在'.format(log_conf_file=log_conf_file)
        raise FileNotFoundError(err_msg)
    logging.config.fileConfig(log_conf_file, disable_existing_loggers=False)
    __logger = logging.getLogger(name=logger_name)
    return __logger