if __name__ == '__main__':
    with open('message', 'rb') as f:
        while True:
            w = f.read(1)
            if not w:
                break
            print(ord(w))
