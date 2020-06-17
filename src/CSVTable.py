import chardet
import pandas as pd

from src.DataTable import DataTable


class CSVTable(DataTable):
    def __init__(self, file_path, root_dir):
        DataTable.__init__(self, file_path, root_dir)
        self.type = 'csv'

    def read_file(self):
        print(str(self.file_path) + "  => " + self.name)
        df = pd.DataFrame()
        try:
            with open(self.file_path, 'rb') as rawdata:
                result = chardet.detect(rawdata.read(1024))
            self.encoding = result['encoding']
            df = pd.read_csv(self.file_path, encoding=self.encoding, parse_dates=False)
        except pd.errors.EmptyDataError as e:
            print("File empty: " + str(self.file_path))
            self.headers = []
            # Remove the table
            return
        except UnicodeDecodeError as e:
            # failed to detect try windows encoding
            #print("failed to load " + str(self.file_path) + " ...trying Windows cp1252 encoding")
            self.encoding = 'cp1252'
            df = pd.read_csv(self.file_path, self.encoding, engine='python', parse_dates=False)
        except UserWarning as e:
            pass

        return df

    def write_file(self, conn, sqltext):
        pd.read_sql(sqltext, con=conn).to_csv(self.file_path, index=False)


