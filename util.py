def read_file(src):
    content = None
    with open(src, 'r') as f:
        content = f.read()
    f.closed
    return content
