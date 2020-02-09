import re


class TDOtioEntity:

    @staticmethod
    def make_legal(str_):
        legal_name = re.sub(r"\.|\s", "_", str_)
        return legal_name
