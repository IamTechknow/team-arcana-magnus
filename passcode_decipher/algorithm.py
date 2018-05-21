from enum import Enum
import codecs
from math import fmod
import Consts

class AlgorithmType(Enum) :
    VIGENERE = "VIGENERE"
    ROT13 = "ROT13"
    ATBASH = "ATBASH"
    BASE64 = "BASE64"
    COLTRANS = "COLTRANS" #Column Trasposition
    NONE = "NONE"
    
    
class Algorithm:
    ALPHA = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ascii_min = ord('a')
    ascii_max = ord('z')
    
    def split_len(self, seq, length):
        return [seq[i:i + length] for i in range(0, len(seq), length)]
    
    def get_algo_list(self):
        list = [AlgorithmType.VIGENERE, AlgorithmType.ROT13, AlgorithmType.ATBASH, AlgorithmType.BASE64, AlgorithmType.COLTRANS, AlgorithmType.NONE]
        return list
    
    
    def encrypt(self, type, value):
        print(str(type))
        if (type is AlgorithmType.ROT13) :
            return codecs.encode(value, 'rot_13')
        if (type is AlgorithmType.BASE64) :
            value = codecs.encode(value, 'unicode_internal')
            return "ERROR B64"
        if (type is AlgorithmType.VIGENERE) :
            key = Consts.CRYPTO_KEY_LETTERS
            alpha = ""
            for printable in range(Algorithm.ascii_min, Algorithm.ascii_max+1):
                alpha = alpha + chr(printable)

            # Ensure the key is at least as long as the ciphertext by cat'ing it
            while len(key) < len(value):
               key = key + key
            key = key[0:len(value)]

            out = ""
            for i in range(len(value)):
                index_from_phrase = (ord(value[i]) - Algorithm.ascii_min)
                index_from_key = ord(key[i]) - Algorithm.ascii_min
                difference = (index_from_phrase - index_from_key)

                # We want the sign of the dividend so we use fmod()
                # Use the inverse of this result (I'm not certain why - is there a simpler way?
                intersect = int(fmod(index_from_phrase - index_from_key, (Algorithm.ascii_max - Algorithm.ascii_min + 1)) * -1)

                letter = alpha[intersect]
                out += letter

            return out
        if (type is AlgorithmType.ATBASH) :
            cipher = ""
            for i in value:
                print(i)
                index = Algorithm.ALPHA.index(i)
                cipher += Algorithm.ALPHA[abs(len(Algorithm.ALPHA) - index - 1) % len(Algorithm.ALPHA)]
            return cipher
        if (type is AlgorithmType.COLTRANS) :
            key = Consts.CRYPTO_KEY_NUM
            order = {
                int(val): num for num, val in enumerate(key)
            }

            ciphertext = ''
            for index in sorted(order.keys()):
                for part in self.split_len(value, len(key)):
                    try:
                        ciphertext += part[order[index]]
                    except IndexError:
                        continue

            return ciphertext
        return value
    