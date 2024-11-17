from typing import List
from leetcode import StringOps


class Encoder:
    def __init__(self):
        self.str_operator = StringOps()

    def encode(self, input_str: str) -> str:
        return self.str_operator.compress_str(input_str)

    def decode(self, input_str: str) -> str:
        return self.str_operator.decompress_str(input_str)


class Analyzer:
    def __init__(self):
        self.str_operator = StringOps()

    def get_most_freq_substrs(self, input_str: str) -> tuple[List[str], int]:
        return self.str_operator.get_most_freq_substrs(input_str)
