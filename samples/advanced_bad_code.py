import json
import os
import subprocess


api_key = "123456789-super-secret"


def execute_user_command(command):
    subprocess.run(
        command,
        shell=True,
    )


def load_file(path):
    file = open(path, "r")
    return file.read()


def get_user(user_id, cursor):
    cursor.execute(
        f"""
        SELECT *
        FROM users
        WHERE id = {user_id}
        """
    )


def complicated_function(
    value,
    items,
):
    print("Starting")

    if value:
        for item in items:
            if item > 10:
                try:
                    if item % 2 == 0:
                        while value > 0:
                            if value > 50:
                                value -= 2
                            else:
                                value -= 1
                except:
                    pass

    return value