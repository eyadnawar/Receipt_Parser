import unittest
#from receipts_parser.receipts.file_parser import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def setUp(self) -> None:
        self.file = open('receipt_sample.txt', 'rb').readlines()
        self.delimiter = '-'
        self.str = self.file[0]

    def test_file_parser(self):
        from receipts_parser.receipts.file_parser import file_parser
        result = file_parser(self.file, self.delimiter)
        self.assertTrue(result is not None, msg= "The method returned a non-None result")
        self.assertTrue(isinstance(result,list), msg= "The method returned a list")
        self.assertTrue(len(result) != 0, msg= "The method returned a non-empty list, file is not empty")
        self.assertTrue(len(result) == 27, msg= "correct result for this sample file")

    def test_get_num_of_blocks(self):
        from receipts_parser.receipts.file_parser import file_parser, get_num_of_blocks
        result = get_num_of_blocks(file_parser(self.file, self.delimiter))
        self.assertTrue(result is not None, msg="The method returned a non-None result")
        self.assertTrue(isinstance(result, int), msg="The method returned an integer value")
        self.assertTrue(result == 8, msg= "correct result for this sample file")

    def test_get_row(self):
        from receipts_parser.receipts.file_parser import get_row
        start_row, end_row = get_row(self.file, self.str)
        self.assertTrue(start_row is not None, msg="The method returned a non-None result")
        self.assertTrue(isinstance(start_row, int), msg="The method returned a list")
        self.assertTrue(end_row is not None, msg="The method returned a non-None result")
        self.assertTrue(isinstance(end_row, int), msg="The method returned a list")

    def test_get_cols(self):
        from receipts_parser.receipts.file_parser import file_parser, get_border
        result = get_border(file_parser(self.file, self.delimiter))
        self.assertTrue(result is not None, msg="The method returned a non-None result")
        self.assertTrue(isinstance(result, list), msg="The method returned a list")
        self.assertTrue(len(result) != 0, msg="The method returned a non-empty list.")


if __name__ == '__main__':
    unittest.main()
