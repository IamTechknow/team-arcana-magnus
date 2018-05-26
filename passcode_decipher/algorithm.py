from enum import Enum
import codecs
from math import fmod
import Consts
import re
import binascii
import base64
import random

class AlgorithmType(Enum) :
    #VIGENERE = "VIGENERE"
    ROT13 = "ROT13"
    ATBASH = "ATBASH"
    #BASE64 = "BASE64"
    COLTRANS = "COLTRANS" #Column Trasposition
    REVERSE = "REVERSE"
    KBMIRROR = "KB_MIRROR"
    POLYBIUS = "POLYBIUS"
    LETTERTONUMBER = "LETTER_NUMBER"
    BINARY = "BINARY"
    
class Algorithm:
    ALPHA = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ascii_min = ord('a')
    ascii_max = ord('z')
    
    def split_len(self, seq, length):
        return [seq[i:i + length] for i in range(0, len(seq), length)]
    
    def get_algo_list(self, level):
        full_list = [e for e in AlgorithmType]
        print(full_list)
        list = random.sample(full_list, 6)
        #list = [AlgorithmType.BASE64, AlgorithmType.BASE64, AlgorithmType.BASE64, \
        #        AlgorithmType.BASE64, AlgorithmType.BASE64, AlgorithmType.BASE64]
        #list = [AlgorithmType.BINARY, AlgorithmType.BINARY,AlgorithmType.BINARY, \
        #        AlgorithmType.BINARY, AlgorithmType.BINARY, AlgorithmType.BINARY]
        return list
    
    
    def encrypt(self, type, value):
        print(str(type) + " -" + value)
        if (type is AlgorithmType.ROT13) :
            return codecs.encode(value, 'rot_13')
        elif (type is AlgorithmType.BASE64) :
            #value = codecs.encode(value, 'unicode_internal')
            cipher = base64.b64encode(value.encode('utf-8'))
            return cipher
        elif (type is AlgorithmType.VIGENERE) :
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
        elif (type is AlgorithmType.ATBASH) :
            cipher = ""
            for i in value:
                print(i)
                index = Algorithm.ALPHA.index(i)
                cipher += Algorithm.ALPHA[abs(len(Algorithm.ALPHA) - index - 1) % len(Algorithm.ALPHA)]
            return cipher
        elif (type is AlgorithmType.COLTRANS) :
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
        elif (type is AlgorithmType.REVERSE):
            return value[::-1]
        elif (type is AlgorithmType.KBMIRROR):
            s1 = "1234567890qwertyuiopasdfghjkl;zxcvbnm,./"
            s2 = "qwertyuiop1234567890zxcvbnm,./asdfghjkl;"
            result = ""
            for i in value.lower():
                position = s1.find(i)
                print(str(i) + str(position))
                result+= s2[position]
            return result
        elif (type is AlgorithmType.POLYBIUS):
            result = "TODO"
            array = self.generate_polybius_array("")
            print(array)
            cipher = ''


            for word in value.upper():
                for i in range(len(array)):
                    if word in array[i]:
                        oy = str(i + 1)
                        ox = str((array[i].index(word) + 1))
                        cipher += oy + ox

            return " ".join(cipher[i:i + 2] for i in range(0, len(cipher), 2))
        elif (type is AlgorithmType.LETTERTONUMBER):
            result = ""
            for  char in value:
                temp = 1 + self.ALPHA.index(char)
                if (temp < 10):
                    result += "0" + str(temp)
                else:
                    result += str(temp)
            return " ".join(result[i:i + 2] for i in range(0, len(result), 2))
        elif (type is AlgorithmType.BINARY):
            bits = bin(int(binascii.hexlify(value.encode('utf-8', 'surrogatepass')), 16))[2:]
            return bits.zfill(8 * ((len(bits) + 7) // 8))
        else:
            return value
        
    def generate_polybius_array(self,key=''):

        """Create Polybius square with transposition.
        :param key: transposition word
        :return: array
        """
        alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
        array = []
        _tmp = []
        key = re.sub(r'[^a-zA-Z]+', '', key)  # remove non-alpha character
        key = key.upper()

        if key:
            for k in key:
                alphabet = alphabet.replace(k, '')

            alphabet = key + alphabet

        for y in range(5):
            for x in range(5):
                _tmp.append(alphabet[0 + 5 * y + x])
            array.append(_tmp)
            _tmp = []
        print(array)
        return array
    
