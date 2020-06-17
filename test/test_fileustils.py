import unittest

from src.fileutils import *


class test_fileutils(unittest.TestCase):
    def test_get_csv_list(self):
        csv_list = get_csv_list('data')
        self.assertEqual(str(csv_list[0]), "data\\annual-enterprise-survey.csv")

    def test_get_excel_list(self):
        excel_list = get_excel_list('data')
        self.assertEqual(str(excel_list[0]), "data\Classeur1.xlsx")


