import re
async def hunter_def(d, e, f) -> int:
    charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/"
    source_base = charset[0:e]
    target_base = charset[0:f]

    reversed_input = list(d)[::-1]
    result = 0

    for power, digit in enumerate(reversed_input):
        if digit in source_base:
            result += source_base.index(digit) * e**power

    converted_result = ""
    while result > 0:
        converted_result = target_base[result % f] + converted_result
        result = (result - (result % f)) // f

    return int(converted_result) or 0
async def hunter( h, u, n, t, e, r) -> str:
        i = 0
        result_str = ""
        while i < len(h):
            j = 0
            s = ""
            while h[i] != n[e]:
                s += h[i]
                i += 1

            while j < len(n):
                s = s.replace(n[j], str(j))
                j += 1

            result_str += chr(await hunter_def(s, e, 10) - t)
            i += 1

        return result_str
async def process_hunter_args(hunter_args: str) -> list:
    hunter_args = re.search(r"^\"(.*?)\",(.*?),\"(.*?)\",(.*?),(.*?),(.*?)$", hunter_args)
    processed_matches = list(hunter_args.groups())
    processed_matches[0] = str(processed_matches[0])
    processed_matches[1] = int(processed_matches[1])
    processed_matches[2] = str(processed_matches[2])
    processed_matches[3] = int(processed_matches[3])
    processed_matches[4] = int(processed_matches[4])
    processed_matches[5] = int(processed_matches[5])
    return processed_matches
