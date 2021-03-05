# fryptor
A memory-friendly file encryptor/decryptor.
```commandline
usage: fryptor.py [-h] -i PATH -k KEY [-o PATH]

optional arguments:
  -h, --help           show help message and exit
  -i PATH, --in PATH   path to source file
  -k KEY, --key KEY    key used in encryption/decryption
  -o PATH, --out PATH  path to output file

```
If u wanna process a folder, u need to write another script calling `process()` from `fryptor.py` and customize `dst` for every file included in that folder by yourself.
