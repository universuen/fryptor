from hashlib import md5
from argparse import ArgumentParser
import os


def _key_parser(key: str):
    seed = key.encode()
    while True:
        seed = md5(seed).digest()
        yield seed[0]


def _file_reader(path: str):
    with open(path, 'rb') as f:
        for line in f:
            for byte in line:
                yield byte


def _file_writer(path: str):
    with open(path, 'wb') as f:
        while True:
            int_ = yield
            f.write(bytes([int_]))


def process(src: str, dst: str, key: str):
    replace = False
    if dst is None:
        dst = f'{src}.temp'
        replace = True
        print('Output path not specified, source file will be replaced.')

    fr = _file_reader(src)
    fw = _file_writer(dst)
    pp = _key_parser(key)

    fw.send(None)
    print('Processing')
    for i, j in zip(fr, pp):
        fw.send(i ^ j)
    fw.close()

    if replace:
        os.remove(src)
        os.rename(dst, src)

    print('Done')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-i', '--in', help='path to source file', metavar='PATH', required=True, dest='src')
    parser.add_argument('-k', '--key', help='key used in encryption/decryption', required=True)
    parser.add_argument('-o', '--out', help='path to output file',
                        metavar='PATH', dest='dst')
    args = parser.parse_args()
    if not os.path.exists(args.src):
        raise FileExistsError('Path to source file is wrong!')
    process(args.src, args.dst, args.key)
