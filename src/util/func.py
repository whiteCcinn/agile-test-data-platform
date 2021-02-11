import hashlib


def md5(data):
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()


if __name__ == '__main__':
    print(md5("开发测试"))
