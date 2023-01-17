
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
            ciphertext += chr(ord("A") + (ord(elem) + (ord(keyword[pos % length]) - 2 * ord("A"))) % 26)
        elif elem.islower():
            ciphertext += chr(ord("a") + (ord(elem) + (ord(keyword[pos % length]) - 2 * ord("a"))) % 26)
        else:
            ciphertext += elem
    return ciphertext


def decrypt_vigenere(cipher_text, key):
    result = ""
    length = len(key)
    for pos, elem in enumerate(cipher_text):
        if elem.isupper():
            result += chr(ord("A") + (ord(elem) - ord(key[pos % length])) % 26)
        elif elem.islower():
            result += chr(ord("a") + (ord(elem) - ord(key[pos % length])) % 26)
        else:
            result += elem
    return result
