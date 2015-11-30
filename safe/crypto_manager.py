__author__ = 'sumeet'

import os
import random
import struct
import hashlib
from Crypto.Cipher import AES


class CryptoManager:
    def __init__(self, password):
        """
        TODO: convert to using RSA keypair
        :param password:
                The encryption password.
        """
        self.key = hashlib.sha256(password).digest()

    def encrypt_file(self, in_filename, out_filename=None, chunksize=64*1024):
        """ Encrypts a file using AES (CBC mode) with the
            given key.

            in_filename:
                Name of the input file

            out_filename:
                If None, '<in_filename>.enc' will be used.

            chunksize:
                Sets the size of the chunk which the function
                uses to read and encrypt the file. Larger chunk
                sizes can be faster for some files and machines.
                chunksize must be divisible by 16.
        """
        if not out_filename:
            out_filename = in_filename + '.enc'

        iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
        encryptor = AES.new(self.key, AES.MODE_CBC, iv)
        file_size = os.path.getsize(in_filename)

        with open(in_filename, 'rb') as infile:
            with open(out_filename, 'wb') as outfile:
                outfile.write(struct.pack('<Q', file_size))
                outfile.write(iv)

                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += ' ' * (16 - len(chunk) % 16)

                    outfile.write(encryptor.encrypt(chunk))

    def decrypt_file(self, in_filename, out_filename=None, chunksize=64*1024):
        """ Decrypts a file using AES (CBC mode) with the
            given key.

            in_filename:
                Name of the input file

            out_filename:
                If None, will be in_filename without its last extension
                (i.e. if in_filename is 'aaa.zip.enc' then
                out_filename will be 'aaa.zip')
        """
        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]

        with open(in_filename, 'rb') as infile:
            orig_size = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(self.key, AES.MODE_CBC, iv)

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))

                outfile.truncate(orig_size)

