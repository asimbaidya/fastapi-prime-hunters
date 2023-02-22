def is_prime(n: int) -> bool:
    """
    Simple func to check if a number if prime!
    """
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    i: int = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True
