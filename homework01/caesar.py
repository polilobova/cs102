length = 26
def encrypt_caesar(plaintext: str, shift: int = 3) -> str:

    """

    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")

    'SBWKRQ'

    >>> encrypt_caesar("python")

    'sbwkrq'

    >>> encrypt_caesar("Python3.6")

    'Sbwkrq3.6'

    >>> encrypt_caesar("")

    ''

    """

    ciphertext = ""

    for i in range(len(plaintext)):

        char = plaintext[i]

        if char.isupper():

            ciphertext += chr((ord(char) + shift - ord("A")) % length + ord("A"))

        elif char.islower():

            ciphertext += chr((ord(char) + shift - ord("a")) % length + ord("a"))

        else:

            ciphertext += char

    return ciphertext







def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:

    """

    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")

    'PYTHON'

    >>> decrypt_caesar("sbwkrq")

    'python'

    >>> decrypt_caesar("Sbwkrq3.6")

    'Python3.6'

    >>> decrypt_caesar("")

    ''

    """

    plaintext = ""

    for i in range(len(ciphertext)):

        char = ciphertext[i]

        if char.isupper():

            plaintext += chr((ord(char) - shift - ord("A")) % length + ord("A"))

        elif char.islower():

            plaintext += chr((ord(char) - shift - ord("a")) % length + ord("a"))

        else:

            plaintext += char

    return plaintext