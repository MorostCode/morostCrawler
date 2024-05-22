# -*- coding: utf-8 -*- 
# @Time: 2024/5/21 下午10:21 
# @Author: morost
# @File: migration.py 
# @desc:

import os

from scrapy.utils.project import get_project_settings

# 获取数据库模型文件夹路径
models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")


def generate_migration_command(db_params):
    migration_command = (f"python -m pwiz -e postgres "
                         f"-H {db_params['host']} "
                         f"-p {db_params['port']} "
                         f"-u {db_params['user']} -P "
                         f"{db_params['database']} > "
                         fr"{models_dir}\db_model_{db_params['database']}.py")
    res_str = f"{migration_command}\n{db_params['password']}"
    return res_str


if __name__ == '__main__':
    command = generate_migration_command(get_project_settings().get("DB_PARAMS"))  # 9527
    print(command)
