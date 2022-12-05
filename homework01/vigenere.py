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
