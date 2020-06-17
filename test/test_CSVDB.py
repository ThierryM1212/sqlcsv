import sys
import unittest
import time
import io
from shutil import copyfile

from src.CSVDB import CSVDB
from src.fileutils import get_file_type


class test_CSVDB(unittest.TestCase):
    def setUp(self):
        self.csv_file = 'data/rh/personnes.csv'
        self.root_dir = 'data'

    def test_load_file(self):
        db = CSVDB(self.csv_file)
        type = get_file_type(self.csv_file)
        db.load_file(type, self.csv_file, self.root_dir)

    def test_load(self):
        db = CSVDB(self.root_dir)

    def test_print_sql(self):
        db = CSVDB(self.root_dir)
        result = db.print_sql("select * from rh_personnes")
        self.assertEqual(result, '')

    def test_desc(self):
        db = CSVDB(self.root_dir)
        result = db.desc('rh_personnes')
        self.assertEqual(result, '')

    def test_save_changes_to_csv(self):
        test_tile = self.csv_file + '_test.csv'
        copyfile(self.csv_file, test_tile)
        db = CSVDB(test_tile)
        db.print_sql("update personnes_csv_test set id = 0")
        db.print_sql("commit")
        time.sleep(0.5)
        db = CSVDB(test_tile)
        result = db.execute_sql("select distinct id from personnes_csv_test")
        self.assertEqual(result, [['id'], (0,)])

    def test_get_table_name_list(self):
        db = CSVDB(self.root_dir)
        table_list = db.get_table_name_list()
        self.assertTrue('rh_personnes' in table_list)

    def test_execute_sql(self):
        db = CSVDB(self.root_dir)
        result = db.execute_sql("select 1")
        self.assertEqual(result, [['1'], (1,)])


