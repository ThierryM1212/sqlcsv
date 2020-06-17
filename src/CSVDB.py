import sqlite3
import csv
import sys
import webbrowser

from src import TableFactory
from src.fileutils import *
from prettytable import from_db_cursor


class CSVDB(object):
    database = None
    root_dir = None
    table_list = None
    output_format = None
    output_formats = None
    spool_file = None

    def __init__(self, root_dir):
        self.conn = sqlite3.connect(":memory:")
        self.init_db()
        self.table_list = []
        self.root_dir = root_dir
        if root_dir is not None:
            self.table_list = self.load(self.root_dir)
        self.output_formats = ['pretty', 'csv', 'html']
        self.output_format = 'pretty'
        self.spool_file = None

    def load(self, root_dir):
        print("Loading table(s):")
        result = []
        total_size = 0
        start_time = time.time()
        root_dir = root_dir.replace('"', '')
        if os.path.isfile(root_dir):
            file_type = get_file_type(root_dir)
            result += self.load_file(file_type, root_dir, '')
        else:
            if os.path.isdir(root_dir):
                file_dict = get_all_supported_files(root_dir)
                for file_type in file_dict.keys():
                    for file_name in file_dict[file_type]:
                        total_size += os.path.getsize(file_name)
                        result += self.load_file(file_type, file_name, root_dir)
            else:
                print("Cannot find: " + root_dir)
                return []

        print('Size of loaded files: %s MB -- %s seconds' % (
        round(total_size / (1024 * 1024), 3), round(time.time() - start_time, 3)))

        return result

    def load_file(self, file_type, file_name, root_dir):
        table = TableFactory.get_table(file_type, file_name, root_dir)
        loaded_tables = table.load(self.conn)
        self.table_list += loaded_tables
        return loaded_tables

    def print_sql(self, sql_text):
        # Backup changes in file on commit_files
        if sql_text.lower().strip() in ('commit_files', 'commit_files;'):
            if len(self.get_modified_tables()) == 0:
                return ["No change to commit"]
            # TODO backup files before complete save
            save_file_success = self.save_changes_to_csv()
            if not save_file_success:
                self.conn.rollback()
            else:
                self.conn.commit()
            return [""]

        c = self.conn.cursor()
        c.execute(sql_text)

        # Manage the print output format
        if self.output_format in ["pretty", "html"]:
            x = from_db_cursor(c)
            if x is not None:
                if self.output_format == "pretty":
                    print(x)
                elif self.output_format == "html":
                    web_page = make_html_page(str(x.get_html_string()))
                    if self.spool_file is not None:
                        self.spool_file.write(web_page)
                    else:
                        f = open('temp.html', 'w')
                        f.write(web_page)
                        f.close()
                        webbrowser.open('temp.html')

        if self.output_format == "csv":
            column_names = [i[0] for i in c.description]
            csvwriter = csv.writer(sys.stdout, lineterminator="\n")
            csvwriter.writerow(column_names)
            csvwriter.writerows(c, )

        c.close()

        return ""

    def desc(self, table_name):
        return self.print_sql("SELECT * FROM sqlite_master WHERE name = '" + table_name + "';")

    def init_db(self):
        self.execute_sql("""create table modified_tables (name text not null unique);""")

    def save_changes_to_csv(self):
        result = True
        modified_tables = self.get_modified_tables()

        for row in modified_tables:
            for table in self.table_list:
                if table.type == 'excel' and str(table.name) == str(row[0]) and result:
                    result = table.commit_changes(self.conn)
                else:
                    if str(table.name) == str(row[0]) and result:
                        result = table.commit_changes(self.conn)

        return result

    def set_output_format(self, output_format):
        if output_format not in self.output_formats:
            return ["output format must be in [" + '|'.join(self.output_formats) + "]"]
        self.output_format = output_format
        return ["output format set to " + self.output_format]

    def set_spool_file(self, param):
        if param.lower() == 'off':
            if self.spool_file is None:
                return ["spool to file was not activated"]
            message = ["Stop logging in " + str(self.spool_file.name)]
            self.spool_file.close()
            self.spool_file = None
            sys.stdout = sys.__stdout__
            return message

        self.spool_file = open(param, 'w')
        sys.stdout = self.spool_file
        return [""]

    def get_table_name_list(self):
        result = []
        for n in self.table_list:
            result.append(n.name)
        return result

    def get_modified_tables(self):
        modified_tables = self.execute_sql("select name from modified_tables;")
        modified_tables.pop(0)  # remove header
        return modified_tables

    def print_modified_tables(self):
        return self.print_sql("select name as modified_tables from modified_tables;")

    def execute_sql(self, sql_text):
        c = self.conn.cursor()
        c.execute(sql_text)
        rows = c.fetchall()
        result = []
        if c.description is not None:
            headers = [i[0] for i in c.description]
            result.append(headers)
            for row in rows:
                result.append(row)
        return result
