import heapq
import json


class Tree:
    def __init__(self, parent, left_child=None, right_child=None):
        self.parent = parent
        self.left_child = left_child
        self.right_child = right_child


def cal_freq(s_file):
    freq_list = {}

    for character in s_file:
        if character in freq_list:
            freq_list[character] += 1
        else:
            freq_list.update({character: 1})

    return freq_list


def create_code_list(heap_node):
    code_list = {}
    code = traverse_tree(heap_node, '')

    for key, value in code:
        code_list.update({key: value})

    return code_list


def traverse_tree(heap_node, code_char):
    if isinstance(heap_node[1][1], Tree):
        e_1 = traverse_tree(heap_node[1][1].left_child, code_char + '0')
        e_2 = traverse_tree(heap_node[1][1].right_child, code_char + '1')

        return e_1 + e_2
    else:
        code = [(heap_node[1][1], code_char)]
        return code


def write_binary_encoding(full_bit_encoding, file_name):
    leftover_bits = len(full_bit_encoding) % 8

    with open(file_name, 'wb') as binary_file:
        if leftover_bits != 0:
            full_bit_encoding += '0' * (8 - leftover_bits)

        byte = bytearray(int(full_bit_encoding[i:i + 8], 2) for i in range(0, len(full_bit_encoding), 8))
        binary_file.write(byte)

    return file_name


def write_code_file(code_book, file_name):
    with open(file_name, 'w') as code:
        json.dump(code_book, code)


def create_encoding(freq_dic, s_file):
    # Heapq cannot compare objects, so in the case that we have a tie
    #  the tie is broken with the count variable. Silly, but functional.
    count = 0

    # Using a list a heap sead, we iterate through the freq dic and
    #  create construct the heap node by node.
    m_heap = []
    for key, value in freq_dic.items():
        heapq.heappush(m_heap, (value, (count, key)))
        count += 1

    # While there are two are more nodes in the heap, we pop smallest (by freq)
    #  nodes from the priority queue and combine them.

    #  Example:
    #                    (ac:3) <- newly combined node, re-inserted in heap.
    #                    /    \
    # popped node -> (a:1)  (c:2) <- popped node

    while len(m_heap) > 1:
        count += 1
        node_1 = heapq.heappop(m_heap)
        node_2 = heapq.heappop(m_heap)

        parent_node = node_1[0] + node_2[0]

        if node_1[0] <= node_2[0]:
            tree_data = Tree(parent_node, node_1, node_2)
        else:
            tree_data = Tree(parent_node, node_2, node_1)
        heapq.heappush(m_heap, (parent_node, (count, tree_data)))

    # If there is one node left in the heap, we have successfully combined all
    #  of the previously popped nodes into one huffman tree.
    #  We now iterate over the tree and create the code.
    if len(m_heap) == 1:
        code_book = create_code_list(heapq.heappop(m_heap))

    # Convert the string_file to a list and iterate over each char and replace
    #  with the coresponding code from the code_book.
    encoding = list(s_file)
    for i in range(0, len(encoding)):
        encoding[i] = code_book[encoding[i]]

    # Join the list back to a string and flip the code_book for later use.
    encoding = ''.join(encoding)
    flipped_code_book = dict(zip(code_book.values(), code_book.keys()))
    flipped_code_book.update({'length': len(encoding)})

    return encoding, flipped_code_book


def decode_file(code_book_file, file_name):
    symbol, decoded_file, bit_string = "", "", ""

    with open(code_book_file, 'r') as code:
        code_book = json.load(code)

    with open(file_name, 'rb') as byte_stream:
        for byte in byte_stream.read():
            bit_string += format(byte, '08b')

        # Iterate through specified length so that we don't decode added zeros.
        # Concat bits to a symbol until it matches a code in the code_book.
        for i in range(0, code_book['length']):
            symbol += bit_string[i]

            # If its found, concat with decoded file and reset process.
            if symbol in code_book:
                decoded_file += code_book[symbol]
                symbol = ""
    # print(decoded_file)
    return decoded_file
