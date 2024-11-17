from typing import List


class StringOps:
    def get_substrs(self, input_str: str) -> List[str]:
        substrs = set()
        for i in range(len(input_str)):
            for j in range(i, len(input_str)):
                substrs.add(input_str[i : j + 1])
        return list(substrs)

    def get_substr_cnts(self, input_str: str) -> dict:
        substr_cnt = {}
        for substr in self.get_substrs(input_str):
            substr_cnt[substr] = input_str.count(substr)
        return substr_cnt

    def get_most_freq_substrs(self, input_str: str) -> tuple[List[str], int]:
        substr_cnt = self.get_substr_cnts(input_str)
        max_freq = max(substr_cnt.values())
        freq_substrs = []
        for substr, freq_cnt in substr_cnt.items():
            if freq_cnt == max_freq:
                freq_substrs.append(substr)
        return freq_substrs, max_freq

    # LeetCode: 471. Encode String with Shortest Length
    def _compress_substr(self, input_str: str, dp: dict, i: int, j: int) -> str:
        empty_str = ""
        if i > j:
            return empty_str
        if i == j:
            return input_str[i]
        if dp[(i, j)] == empty_str:
            substr = input_str[i : j + 1]
            dp[(i, j)] = substr
            if j > i + 4:
                for k in range(i, j + 1):
                    left_cmpress = self._compress_substr(input_str, dp, i, k)
                    right_cmpress = self._compress_substr(input_str, dp, k + 1, j)
                    cmpress_combined = left_cmpress + right_cmpress
                    if len(cmpress_combined) < len(dp[(i, j)]):
                        dp[(i, j)] = cmpress_combined
            substr_len = j + 1 - i
            for k in range(i, j):
                pattern_len = k + 1 - i
                if substr_len % pattern_len == 0:
                    pattern = input_str[i : k + 1]
                    if substr.replace(pattern, empty_str) == empty_str:
                        cmpress_pattern = self._compress_substr(input_str, dp, i, k)
                        pattern_cnt = substr_len // pattern_len
                        cmpress_substr = str(pattern_cnt) + "[" + cmpress_pattern + "]"
                        if len(cmpress_substr) < len(dp[(i, j)]):
                            dp[(i, j)] = cmpress_substr
        return dp[(i, j)]

    def compress_str(self, input_str: str) -> str:
        dp = {}
        for i in range(len(input_str)):
            for j in range(i, len(input_str)):
                dp[(i, j)] = ""
        first_index = 0
        last_index = len(input_str) - 1
        return self._compress_substr(input_str, dp, first_index, last_index)

    # LeetCode: 394. Decode String
    def decompress_str(self, input_str: str) -> str:
        count_stack = []
        char_stack = []
        i = 0
        while i < len(input_str):
            num = 0
            while i < len(input_str) and input_str[i].isnumeric():
                num = num * 10 + int(input_str[i])
                i += 1
            if num != 0:
                count_stack.append(num)
            if input_str[i] == "]":
                rep_str = ""
                char_st_top = char_stack.pop()
                while len(char_stack) > 0 and char_st_top != "[":
                    rep_str = char_st_top + rep_str
                    char_st_top = char_stack.pop()
                rep = count_stack.pop()
                char_stack.append(rep_str * rep)
            else:
                char_stack.append(input_str[i])
            i += 1
        return "".join(char_stack)
