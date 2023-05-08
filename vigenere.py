import re


def encrypt(msg: str, key: str) -> str:

    """
    Encrypts the given message with the given key by using the Vigenere cipher.
    :param msg: The message that should be encrypted.
    :param key: The key that should be used to encrypt the message.
    :return: Returns the encrypted message.
    """

    # ensure that msg only contains lower case letters
    msg = msg.lower()
    msg = "".join(re.findall("[a-z]+", msg))  # removing non-allowed subgroups

    n = 26  # indicates, that the alphabet of 26 letters should be used

    encrypted_msg = ""
    key_len = len(key)
    for index in range(len(msg)):
        # ensure that the real Vigenere square is used
        # e.g. replace 'a' (ASCII 97) with 0, encrypt it, and transfer it back by adding 97
        enrypted_symbol = chr(((ord(msg[index]) - 97) + (ord(key[index % key_len]) - 97)) % n + 97)
        encrypted_msg += enrypted_symbol

    return encrypted_msg.upper()


if __name__ == "__main__":

    key = "datensicherheit"

    plain_text_file = open("plain_text", "r")
    cipher_text = encrypt(plain_text_file.read(), key)
    plain_text_file.close()

    cipher_text_file = open("cipher_text", "w")
    cipher_text_file.write(cipher_text)
    cipher_text_file.close()
