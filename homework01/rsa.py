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


def modif(evclid_1: int, phi: int) -> tp.Union[tp.Tuple[int, int, int], int]:
    """necessary modifications before performing multiplicative_inverse"""
    if evclid_1 == 0:
        return phi, 0, 1
    else:
        res, y_0, x_0 = modif(phi % evclid_1, evclid_1)  # type: ignore
        return res, x_0 - (phi // evclid_1) * y_0, y_0


def multiplicative_inverse(evclid_1, evclid_2):
    """
    Euclid's extended algorithm for finding the multiplicative
    inverse of two numbers.
    >>> multiplicative_inverse(7, 40)
    23
    """
    res, x_0, y_0 = modif(evclid_1, evclid_2)
    if res != 1:
        raise Exception("problem")
    else:
        return x_0 % evclid_2


def generate_keypair(first: int, second: int) -> tp.Tuple[tp.Tuple[int, int], tp.Tuple[int, int]]:
    """generating keypair for chipher"""
    if not (is_prime(first) and is_prime(second)):
        raise ValueError("Both numbers must be prime.")
    elif first == second:
        raise ValueError("first and second cannot be equal")
    # num = pq
    num = first * second
    # phi = (p-1)(q-1)
    phi = (first - 1) * (second - 1)
    # Choose an integer evclid such that evclid and phi(num) are coprime
    evclid = random.randrange(1, phi)
    # Use Euclid's Algorithm to verify that evclid and phi(num) are coprime
    res = gcd(evclid, phi)
    while res != 1:
        evclid = random.randrange(1, phi)
        res = gcd(evclid, phi)
    # Use Extended Euclid's Algorithm to generate the private key
    delit = multiplicative_inverse(evclid, phi)
    # Return public and private keypair
    # Public key is (evclid, num) and private key is (delit, num)
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
