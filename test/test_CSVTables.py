import unittest
from shutil import copyfile
from src.CSVDB import CSVDB
from src.CSVTable import CSVTable


class test_CSVTables(unittest.TestCase):
    def setUp(self):
        self.csv_file = 'data/rh/personnes.csv'
        self.root_dir = 'data'
        self.db = CSVDB(self.root_dir)

    def test_str(self):
        table = CSVTable(self.csv_file, self.root_dir)
        self.assertEqual(str(table), 'Table: rh_personnes')

    def test_load(self):
        table = CSVTable(self.csv_file, self.root_dir)
        table.load(self.db.conn)
        self.assertEqual(table.name, 'rh_personnes')
        self.assertEqual(table.headers, ['id', 'name', 'firstname', 'age', 'gender'])
        c = self.db.conn.cursor()
        c.execute("select name from " + table.name)
        rows = c.fetchall()
        c.close()
        self.assertEqual(rows, [('John',), ('Tina',), ('Jean',)])

    def test_commit_changes(self):
        test_tile = self.csv_file+'_test.csv'
        copyfile(self.csv_file, test_tile)
        table = CSVTable(test_tile, self.root_dir)
        table.load(self.db.conn)
        c = self.db.conn.cursor()
        c.execute("update " + table.name + " set id = 0")
        c.execute("commit")
        table.commit_changes(self.db.conn)
        table.load(self.db.conn)
        c.execute("select * from " + table.name)
        rows = c.fetchall()
        print(rows)
        self.assertEqual(rows, [(0, 'John', 'Malkovick', 57, 'M'), (0, 'Tina', 'Turner', 72, 'F'), (0, 'Jean', 'Dubois', 23, 'M')])


if __name__ == '__main__':
    unittest.main()
