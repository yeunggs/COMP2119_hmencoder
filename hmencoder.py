import sys
from collections import Counter


class Node:
    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def is_leaf(self):
        return self.left is None and self.right is None


def generate_codes(node, current_code, huffman_codes):
    if not node:
        return

    if node.is_leaf():
        huffman_codes[node.symbol] = current_code
        return

    generate_codes(node.left, current_code + "0", huffman_codes)
    generate_codes(node.right, current_code + "1", huffman_codes)


def calculate_average(frequency_table, huffman_codes, total_symbols):
    total_bits = sum(frequency_table[char] * len(huffman_codes[char]) for char in frequency_table)
    return total_bits / total_symbols


def huffman_encode(input_file):
    with open(input_file, 'r') as file:
        message = file.read()

    #Count each symbol in original message 
    frequency_table = Counter(message)

    forest = []
    for symbol, frequency in frequency_table.items():
        new_node = Node(symbol, frequency)
        forest.append(new_node)

    #Build Huffman tree using bottom-up approach
    while len(forest) > 1:
        forest.sort(key=lambda x: x.frequency)
        t1 = forest.pop(0)
        t2 = forest.pop(0)

        new_tree = Node(None, t1.frequency + t2.frequency)
        new_tree.left = t1
        new_tree.right = t2

        forest.append(new_tree)

    root = forest[0]
    huffman_codes = {}
    generate_codes(root, "", huffman_codes)

    #Calculate average bits
    total_symbols = len(message)
    average_bits = calculate_average(frequency_table, huffman_codes, total_symbols)

    #Output1: code.txt
    with open("code.txt", "w") as code_file:
        for symbol in sorted(huffman_codes.keys(), key=lambda x: ord(x)):
            if symbol == " ":
                code_file.write(f"Space: {huffman_codes[symbol]}\n")
            elif symbol == "\n":
                code_file.write(f"\\n: {huffman_codes[symbol]}\n")
            else:
                code_file.write(f"{symbol}: {huffman_codes[symbol]}\n")
        code_file.write(f"Ave = {average_bits:.2f} bits per symbol\n")

    #Output2: encodemsg.txt
    encoded_message = "".join(huffman_codes[char] for char in message)
    with open("encodemsg.txt", "w") as encodemsg_file:
        for i in range(0, len(encoded_message), 80):
            encodemsg_file.write(encoded_message[i:i+80] + "\n")


#Main
input_file = sys.argv[1]
huffman_encode(input_file)
