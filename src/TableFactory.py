from src.CSVTable import CSVTable
from src.Excel_File import Excel_File


def get_table(file_type, file_path, root_dir):
    if file_type == 'csv':
        return CSVTable(file_path, root_dir)
    if file_type == 'excel':
        return Excel_File(file_path, root_dir)
    else:
        raise ValueError("type must be csv or excel, actual: " + file_type)
