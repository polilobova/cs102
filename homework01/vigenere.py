Up_start = ord("A")
Low_start = ord("a")
Length = 26

def encrypt_vigenere(plain_text, key):
    result = ""
    length = len(key)
    for pos, elem in enumerate(plain_text):
        if elem.isupper():
            result += chr(Up_start + (ord(elem) + (ord(key[pos%length]) - 2 * Up_start)) % Length)
        elif elem.islower():
            result += chr(Low_start + (ord(elem) + (ord(key[pos%length]) - 2 * Low_start)) % Length)
        else:
            result += elem
    return result


def decrypt_vigenere(cipher_text, key):
    result = ""
    length = len(key)
    for pos, elem in enumerate(cipher_text):
        if elem.isupper():
            result += chr(Up_start + (ord(elem) - ord(key[pos%length])) % Length)
        elif elem.islower():
            result += chr(Low_start + (ord(elem) - ord(key[pos%length])) % Length)
        else:
            result += elem
    return result

string, key = input(), input()
#print(encrypt_vigenere(string, key))
print(decrypt_vigenere(string, key))