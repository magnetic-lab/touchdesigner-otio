import re


class TDOtioEntity:

    @staticmethod
    def _make_legal(str_):
        legal_name = re.sub(r"\W|\s", "_", str_)
        return legal_name

    @staticmethod
    def _decode_url(url):
        return url.replace("file://localhost/", "").replace("%3a", ":")
