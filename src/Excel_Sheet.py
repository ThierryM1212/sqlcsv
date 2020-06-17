from src.DataTable import DataTable
from src.fileutils import compute_table_name


class Excel_Sheet(DataTable):
    def __init__(self, file_path, root_dir, sheet_name, dataframe):
        DataTable.__init__(self, file_path, root_dir)
        self.sheet_name = sheet_name
        self.dataframe = dataframe
        self.headers = list(self.dataframe)
        self.parent_name = compute_table_name(file_path, root_dir)
        self.name = self.parent_name + "$" + self.sheet_name
        self.type = 'excel_sheet'


    def load(self, conn):
        self.dataframe.to_sql(self.name, conn, if_exists='replace', index=False)
        self.create_logging_triggers(conn)
        return [self]

    def create_logging_triggers(self, conn):
        c = conn.cursor()
        for action in ['insert', 'update', 'delete']:
            sql = F"create trigger {self.name}_{action} {action} on {self.name} "
            sql += F"begin insert or ignore into modified_tables values ('{self.parent_name}');end;"
            c.execute(sql)
        c.close()


