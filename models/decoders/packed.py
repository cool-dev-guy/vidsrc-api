import re
async def unpack(p, a, c, k, e=None, d=None) -> str:
    for i in range(c - 1, -1, -1):
        if k[i]: p = re.sub("\\b" + await int_2_base(i, a) + "\\b", k[i], p)
    return p
async def int_2_base(x: int, base: int) -> str:
    charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/"

    if x < 0:
        sign = -1
    elif x == 0:
        return 0
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(charset[int(x % base)])
        x = int(x / base)
        
    if sign < 0:
        digits.append('-')
    digits.reverse()

    return ''.join(digits)

async def process_packed_args(context):
    matches = re.search(r'return p}\((.+)\)', context)
    processed_matches = []
    split_matches = matches.group(1).split(",")
    corrected_split_matches = [",".join(split_matches[:-3])] + split_matches[-3:]
    for val in corrected_split_matches:
      val = val.strip()
      val = val.replace(".split('|'))", "")
      if val.isdigit() or (val[0] == "-" and val[1:].isdigit()):
        processed_matches.append(int(val))
      elif val[0] == "'" and val[-1] == "'":
        processed_matches.append(val[1:-1])

    processed_matches[-1] = processed_matches[-1].split("|")
    return processed_matches
