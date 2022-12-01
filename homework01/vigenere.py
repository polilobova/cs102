Up_start = ord("A")
Low_start = ord("a")
Length = 26

def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    length = len(keyword)
    for pos, elem in enumerate(plaintext):
        if elem.isupper():
            ciphertext += chr(Up_start + (ord(elem) + (ord(keyword[pos%length]) - 2 * Up_start)) % Length)
        elif elem.islower():
            ciphertext += chr(Low_start + (ord(elem) + (ord(keyword[pos%length]) - 2 * Low_start)) % Length)
        else:
            ciphertext += elem
    return ciphertext


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

def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    length = len(keyword)
    for pos, elem in enumerate(cipher_text):
        if elem.isupper():
            ciphertext += chr(Up_start + (ord(elem) - ord(keyword[pos%length])) % Length)
        elif elem.islower():
            ciphertext += chr(Low_start + (ord(elem) - ord(keyword[pos%length])) % Length)
        else:
            ciphertext += elem
    return plaintext

