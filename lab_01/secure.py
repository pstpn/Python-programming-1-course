def secure_five(b: str):
    try:
        float(b)
    except ValueError:
        return False
    if b[0] == '-':
        b = b[1:]
    for i in b:
        if i not in ['0', '1', '2', '3', '4', '.']:
            return False
    return True
