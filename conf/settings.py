#!coding:utf-8
from tornado.options import options, define

define('mysql_host', default='127.0.0.1', help='mysql server ip', type=str)
define('mysql_port', default=3306, help='mysql server port', type=int)
define('mysql_user', default='root', help='mysql server user', type=str)
define('mysql_password', default='5Love1124', help='mysql server password', type=str)
define("port", default=9527, help="run on the given port", type=int)
_app_settings = {}


def init_app_settings():
    """ 命令行参数优先, 会覆盖配置文件中的参数。
    """
    global _app_settings
    if _app_settings:
        return _app_settings
    # 只为了获取 options.config, 后边会再次调用.
    options.parse_command_line(final=False)
    config_file_path = options.config
    if config_file_path:
        options.parse_config_file(config_file_path, final=False)
    options.parse_command_line(final=False)
    options.run_parse_callbacks()
    _app_settings = options.as_dict()
    return _app_settings


def get_app_settings():
    global _app_settings
    if not _app_settings:
        _app_settings = init_app_settings()
    return _app_settings


if __name__ == '__main__':
    kwargs = init_app_settings()
    print kwargs
