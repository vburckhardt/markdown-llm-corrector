import getpass
import random
import string
import os


class Utils:
    @staticmethod
    def generate_random_name(length=8):
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    @staticmethod
    def get_env_variable(var_name, prompt_message):
        return os.environ.get(var_name) or getpass.getpass(prompt_message)