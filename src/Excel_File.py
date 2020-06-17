import pandas as pd
import warnings

from src.DataTable import DataTable
from src.Excel_Sheet import Excel_Sheet

warnings.filterwarnings("ignore")


class Excel_File(DataTable):
    def __init__(self, file_path, root_dir):
        DataTable.__init__(self, file_path, root_dir)
        self.sheet_dict = {}
        self.headers = []
        self.type = 'excel'
        self.sheet_list = []
        self.datemode = None

    def read_file(self):
        print(str(self.file_path) + "  => " + self.name)
        xl = pd.ExcelFile(self.file_path)

        for sheet in xl.sheet_names:
            self.sheet_dict[sheet] = pd.read_excel(xl, sheet_name=sheet, dtype=object)

    def write_file(self, conn, sqltext):
        writer = pd.ExcelWriter(self.file_path, engine='xlsxwriter', datetime_format='mmmm-dd-yyyy', date_format='mmmm-dd-yyyy')
        for sheet in self.sheet_list:
            sqltext = "select * from " + sheet.name
            pd.read_sql(sqltext, con=conn).to_excel(writer, index=False, sheet_name=sheet.sheet_name)
        writer.save()

    def load(self, conn):
        self.read_file()
        result = [self]
        for sheet in self.sheet_dict.keys():
            xl_sheet = Excel_Sheet(self.file_path, self.root_dir, sheet, self.sheet_dict[sheet])
            result += xl_sheet.load(conn)
            self.sheet_list.append(xl_sheet)
        return result


