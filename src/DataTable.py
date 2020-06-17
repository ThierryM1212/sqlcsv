import os
import shutil
from abc import ABC

from src.fileutils import compute_table_name, get_file_type, get_backup_file


class DataTable(ABC):
    def __init__(self, file_path, root_dir):
        self.file_path = file_path
        self.root_dir = root_dir
        self.name = compute_table_name(file_path, root_dir)
        self.headers = None
        self.dialect = None
        self.encoding = None
        self.type = get_file_type(self.file_path)

    def __str__(self):
        message = 'Table: ' + self.name
        return message

    def load(self, conn):
        df = self.read_file()
        if df is not None:
            self.headers = list(df.columns.values)
            df.to_sql(self.name, conn, if_exists='replace', index=False)
            self.create_logging_triggers(conn)
        return [self]

    def create_logging_triggers(self, conn):
        c = conn.cursor()
        for action in ['insert', 'update', 'delete']:
            sql = F"create trigger {self.name}_{action} {action} on {self.name} "
            sql += F"begin insert or ignore into modified_tables values ('{self.name}');end;"
            c.execute(sql)
        c.close()

    def commit_changes(self, conn):
        result = False
        print("Saving: " + str(self.file_path))
        sql = "select * from " + self.name
        try:
            self.backup_file()
            self.write_file(conn, sql)
        except:
            print("Failed to save file " + self.name + ". Rollback issued.")
            c = conn.cursor()
            c.execute("rollback;")
            c.close()
            raise
        else:
            c = conn.cursor()
            c.execute("delete from modified_tables where name = '"+self.name+"';")
            c.close()
            result = True
        return result

    def write_file(self, c, sql):
        pass

    def read_file(self):
        pass

    def backup_file(self):
        full_path = str(os.path.abspath(self.file_path))
        full_backup_path = get_backup_file(full_path)
        shutil.copy(full_path, full_backup_path)
        print('File backup before commit: ' + full_backup_path)
