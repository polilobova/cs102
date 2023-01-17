"""rsa code"""
import random
import typing as tp


def is_prime(num: int) -> bool:
    """
    Tests to see if a number is prime.
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    if num <= 1 or (num > 2 and num % 2 == 0):
        return False
    for delitel in range(3, int(num ** (1 / 2)) + 1, 2):
        if num % delitel == 0:
            return False
    return True


def gcd(num_1: int, num_2: int) -> int:
    """
    Euclid's algorithm for determining the greatest common divisor.
    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    if num_2 == 0:
        return num_1
    while num_1 % num_2 != 0:
        num_1, num_2 = num_2, num_1 % num_2
    return num_2


def multiplicative_inverse(e_num, phi):
    """
    Euclid's extended algorithm for finding the multiplicative
    inverse of two numbers.
    >>> multiplicative_inverse(7, 40)
    23
    """
    nom_1, nom_2 = phi, e_num
    x_var, y_var = 0, 1
    while nom_2:
        div = nom_1 // nom_2
        nom_1, nom_2 = nom_2, nom_1 % nom_2
        x_var, y_var = y_var, x_var - y_var * div
    return x_var % phi


def generate_keypair(first: int, second: int) -> tp.Tuple[tp.Tuple[int, int], tp.Tuple[int, int]]:
    """generating keypair for chipher"""
    if not (is_prime(first) and is_prime(second)):
        raise ValueError("Both numbers must be prime.")
    elif first == second:
        raise ValueError("first and second cannot be equal")
    num = first * second
    phi = (first - 1) * (second - 1)
    evclid = random.randrange(1, phi)
    res = gcd(evclid, phi)
    while res != 1:
        evclid = random.randrange(1, phi)
        res = gcd(evclid, phi)
    delit = multiplicative_inverse(evclid, phi)
    return ((evclid, num), (delit, num))


def encrypt(prov_key: tp.Tuple[int, int], plaintext: str) -> tp.List[int]:
    """encripting plaintext"""
    # Unpack the key into it's components
    key, num = prov_key
    # Convert each letter in the plaintext to numbers based on
    # the character using a^b mod m
    cipher = [(ord(char) ** key) % num for char in plaintext]
    # Return the array of bytes
    return cipher


def decrypt(provkey: tp.Tuple[int, int], ciphertext: tp.List[int]) -> str:
    """decripting a chiphertext"""
    # Unpack the key into its components
    key, num = provkey
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char**key) % num) for char in ciphertext]
    # Return the array of bytes as a string
    return "".join(plain)


if __name__ == "__main__":
    print("RSA Encrypter/ Decrypter")
    num_a = int(input("Enter a prime number (17, 19, 23, etc): "))
    num_b = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(num_a, num_b)
    print("Your public key is ", public, " and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print("".join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypting message with public key ", public, " . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))
