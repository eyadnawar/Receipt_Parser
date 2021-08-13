from django.conf import settings
from django.core.files import uploadedfile
from django.core.files.base import File

def file_parser(file, delimiter):
    """
    A method that takes in a list of all lines (bytes coded) and returns a list of lists where each list is a block
    :param file: file.readlines(): a list of all lines (bytes coded)
    :param delimiter: the separator character eg: '-'
    :return: list of lists where each list is a block in the receipt file
    """
    big_list = []
    small_list = []

    for i in range(0, len(file) - 1):
        if(file[i + 1].decode('utf-8').startswith('\r') or file[i + 1].decode('utf-8').startswith('\n') or file[i + 1].decode('utf-8').startswith(delimiter) or file[i + 1][:-2].decode('utf-8').endswith(delimiter)):
            if (file[i].decode('utf-8').startswith('\r') or file[i].decode('utf-8').startswith('\n') or file[i].decode('utf-8').startswith(delimiter) or file[i][:-2].decode('utf-8').endswith(delimiter)):
                big_list.append([])
            else:
                small_list.append(file[i][:-2].decode('utf-8'))
                big_list.append(small_list)
                small_list = []
        else:
            if (file[i].decode('utf-8').startswith('\r') or file[i].decode('utf-8').startswith('\n') or file[i].decode('utf-8').startswith(delimiter) or file[i][:-2].decode('utf-8').endswith(delimiter)):
                big_list.append([])
            else:
                small_list.append(file[i][:-2].decode('utf-8'))


    if(len(small_list) != 0):
        if(file[-1].decode('utf-8').startswith('\r') or file[-1].decode('utf-8').startswith('\n') or file[-1].decode('utf-8').startswith(delimiter) or file[-1][:-2].decode('utf-8').endswith(delimiter)):
            big_list.append(small_list)
            big_list.append([])
        else:
            small_list.append(file[-1][:-2].decode('utf-8'))
            big_list.append(small_list)
    else:
        if (file[-1].decode('utf-8').startswith('\r') or file[-1].decode('utf-8').startswith('\n') or file[-1].decode('utf-8').startswith('-') or file[-1][:-2].decode('utf-8').endswith('-')):
            big_list.append([])
        else:
            big_list.append([file[-1][:-2].decode('utf-8')])

    return big_list

def get_num_of_blocks(big_list):
    """
    A method to get the number of blocks from the receipt file
    :param big_list: A list of lists, where each sublist is a block of the file, some sublists are empty, they represent an empty block
    :return: the number of blocks in the receipt (int)
    """
    count = 0
    for i in range(0, len(big_list)):
        if (len(big_list[i]) != 0):
            count += 1

    return  count

def get_row(big_list, str):
    """
    A method to get the begin_row and end_row for a specific block
    :param big_list: A list of lists, where each sublist is a block of the file, some sublists are empty, they represent an empty block
    :param str: a string from a block to match the condition
    :return: the start and end row for a speific block
    """
    start_row = 0
    for i in range(0, len(big_list)):
        if(str in big_list[i]):
            if(i == 0):
                end_row = len(big_list[0]) - 1
                break
            else:
                for j in range(0, i):
                    if(len(big_list[j]) == 0):
                        start_row += 1
                    else:
                        start_row += len(big_list[j])
                end_row = start_row + len(big_list[i]) - 1
        else:
            continue

    return start_row, end_row

def get_border(big_list):
    """
    A method to calculate the start and end of a column of a block and return the border of a block
    :param big_list: A list of lists, where each sublist is a block of the file, some sublists are empty, they represent an empty block
    :return: overall border of a block
    """
    blocks = []
    min_col = 1e5
    max_col = -1
    for list in big_list:
        min_col = 1e5
        max_col = -1
        if(len(list) == 0):
            continue
        else:
            for string in list:
                for character in range(0, len(string)):
                    if(string[character] != " "):
                        if(character <= min_col):
                            min_col = character
                        if(character >= max_col):
                            max_col = character + 1
                    else:
                        continue

        start_row, end_row = get_row(big_list, list[0])
        blocks.append({
            "begin_row": start_row,
            "begin_col": min_col,
            "end_row": end_row,
            "end_col": max_col
        })

    return blocks