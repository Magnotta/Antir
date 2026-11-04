def clamp(value, min_val, max_val):
    return int(max(min(value, max_val), min_val))


def expm(exp: int, k: int) -> float:
    return exp / (exp + k)
