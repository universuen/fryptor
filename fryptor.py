from hashlib import md5
from argparse import ArgumentParser
import logging
from threading import Thread
import os

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

_total = 0
_count = 0


def _key_parser(key: str):
    seed = key.encode()
    ptr = 0
    while True:
        while ptr < len(seed):
            yield seed[ptr]
            ptr += 1
        ptr = 0
        seed = md5(seed).digest()


def _file_reader(path: str):
    global _total
    global _count
    _total = os.path.getsize(path)
    with open(path, 'rb') as f:
        while _count < _total:
            yield ord(f.read(1))
            _count += 1


def _file_writer(path: str):
    with open(path, 'wb') as f:
        while True:
            data = yield
            f.write(bytes([data]))


def process(src: str, dst: str, key: str):
    replace = False
    if dst is None:
        dst = f'{src}.temp'
        replace = True

    fr = _file_reader(src)
    fw = _file_writer(dst)
    pp = _key_parser(key)

    fw.send(None)
    for i, j in zip(fr, pp):
        fw.send(i ^ j)
    fw.close()

    if replace:
        os.remove(src)
        os.rename(dst, src)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-i', '--in', help='path to source file', metavar='PATH', required=True, dest='src')
    parser.add_argument('-k', '--key', help='key used in encryption/decryption', required=True)
    parser.add_argument('-o', '--out', help='path to output file', metavar='PATH', dest='dst')
    args = parser.parse_args()
    if not os.path.exists(args.src):
        raise FileExistsError('Path to source file is wrong!')
    if args.dst is None:
        logging.warning('Output path not specified, source file will be replaced.')


    def bar():
        global _total
        global _count
        while _total == 0:
            pass
        while _count < _total:
            print(f'{100 * _count / _total: .2f} %', end='\r')
        print(f'{100 * _count / _total: .2f} %')


    threads = [
        Thread(target=process, args=(args.src, args.dst, args.key)),
        Thread(target=bar),
    ]

    logging.info('Started processing')

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    logging.info('Done')
