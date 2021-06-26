import hashlib


def headhash(path: str, head=512 * 1024) -> str:
    h = hashlib.md5()
    
    with open(path, 'rb') as input:
        input = input.read(head)

    h.update(input)

    return h.hexdigest()