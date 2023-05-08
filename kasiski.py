from sympy.ntheory import factorint


def factorint_to_string(factors: dict) -> str:
    factorization = []
    for base, exp in zip(factors.keys(), factors.values()):
        factorization.append(f"{base}^{exp}")
    return " * ".join(factorization)


def find_repetitions(encrypted_msg: str, min_length: int, max_length: int) -> dict:

    """
    Find the repetitions from min_length <= length < max_length and return their distances.
    Returned dict will be of from: {repetition: [dist1, dist2, ...], ...}.
    :param encrypted_msg: Is the message encrypted by the Vigenere cipher.
    :param min_length: Minimum length of repetitions.
    :param max_length: Maximum length of repetitions (exclusive).
    :return: A dictionary of from: {repetition: [dist1, dist2, ...], ...}.
    """

    # finding the repetitions

    msg_len = len(encrypted_msg)
    repetitions = {}

    for length in range(min_length, max_length):
        already_found = {}
        for cur_index in range(len(encrypted_msg) - length + 1):  # we must include the starting index
            if cur_index + length - 1 < msg_len:  # we must include the starting index
                current_str = encrypted_msg[cur_index:cur_index + length]
                if current_str in already_found.keys():
                    if current_str in repetitions.keys():
                        repetitions[current_str].append(cur_index - already_found[current_str])
                    else:
                        repetitions[current_str] = [cur_index - already_found[current_str]]
                else:
                    already_found[current_str] = cur_index

    return repetitions


def kasiski(encrypted_msg: str, min_length: int, max_length: int) -> dict:

    """
    Applies the Kasiski test to decrypt the Vigenere cipher.
    :param encrypted_msg: Is the message encrypted by the Vigenere cipher.
    :param min_length: Minimum length of repetitions.
    :param max_length: Maximum length of repetitions (exclusive).
    :return: Returns a dictionary of repetitions and their distances
    saved as {repetition: [dist1, dist2, ...], ...}.
    """

    repetitions = find_repetitions(encrypted_msg, min_length, max_length)

    # printing the repetitions

    for rep in repetitions:
        print(f"{rep}:")
        for distance in repetitions[rep]:
            print(f"\t{distance} = {factorint_to_string(factorint(distance))}")

    return repetitions


def number_primefactors(repetitions: dict) -> list:
    """

    :param repetitions: Dictionary of repetitions saved as {repetition: [dist1, dist2, ...], ...}.
    :return: A list of the factors and their occurrences saved as [(factor1, occurrence1), ...].
    Prints the primefactors of the distances ranked by their number of occurrences.
    """

    factors = {}

    for distances in repetitions.values():
        for distance in distances:
            factorized = factorint(distance)
            for base, exp in zip(factorized.keys(), factorized.values()):
                if base not in factors.keys():
                    factors[base] = exp
                else:
                    factors[base] += exp

    factors_list = [(factor, occurrences) for factor, occurrences in factors.items()]
    factors_list.sort(key=lambda elem: elem[1], reverse=True)

    return factors_list


def blockify(msg: str, b: int) -> list:

    """
    Splits the message into blocks where the index mod b-th symbol belongs to the b-th block.
    :param msg: The message which should be split.
    :param b: Specifies the number of blocks and which symbol belongs to which block.
    :return: Returns a list of the newly created blocks.
    """

    blocks = ["" for _ in range(b)]
    for index in range(len(msg)):
        symbol = msg[index]
        blocks[index % b] += symbol
    return blocks


def visualize_blocks(blocks: list, n: int) -> None:
    """

    :param blocks: List of blocks.
    :param n: Number of symbols that should be displayed.
    :return: Nothing. Prints and visualizes the blocks (e.g. occurrences of symbols).
    """

    for id, block in enumerate(blocks):
        print(f"Block no. {id+1}:")
        print(block)
        occurrences = []
        for ascii in range(65, 91):
            occurrences.append((chr(ascii), block.count(chr(ascii))))
        occurrences.sort(key=lambda elem: elem[1], reverse=True)
        for index in range(n):
            print(f"\t{occurrences[index][0]} -> {occurrences[index][1]}")


def swap_letters(block: str, c: str, d: str) -> str:

    """
    Swaps the given letter c to the specified letter d in the given block.
    :param block: The block in which the c should be swapped with d.
    :param c: The character that should be swapped.
    :param d: The character that should replace c.
    :return: Returns the block with the swapped letters.
    """

    return block.replace(c, d)


def decrypt(msg: str, key: str) -> str:

    """
    Decrypts the given message with the given key.
    :param msg: The message that should be decrypted.
    :param key: The key that should be used to decrypt the message.
    :return: Returns the decrypted message as a string.
    """

    # ensure that msg only contains lower case letters (same as encryption)
    msg = msg.lower()

    n = 26  # indicates, that the alphabet of 26 letters should be used

    decrypted_msg = ""
    key_len = len(key)
    for index in range(len(msg)):
        # ensure that the real Vigenere square is used
        decrypted_symbol = chr(((ord(msg[index]) - 97) - (ord(key[index % key_len]) - 97)) % n + 97)
        decrypted_msg += decrypted_symbol

    return decrypted_msg


if __name__ == "__main__":
    cipher_text = open("cipher_text", "r").read()
    repetitions = kasiski(cipher_text, 2, 6)
    print(number_primefactors(repetitions))
    blocks = blockify(cipher_text, 15)
    visualize_blocks(blocks, 10)
    print(decrypt(cipher_text, "datensicherheit"))
