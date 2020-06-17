import sys
import argparse

from src.CSVDB import CSVDB
from pygments.lexers.sql import SqlLexer
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory


sql_csv_keywords = [
    # sqlcsv commands
    'list', 'desc', 'load', 'spool', 'commit_files',
    'output', 'pretty', 'csv', 'html',
    # internal table
    'modified_tables',
    # SQL Lite 3 principal SQL commands
    'select', 'from', 'insert', 'update', 'delete', 'set',
    'case', 'when', 'cast', 'count', 'group by', 'order by',
    'isnull', 'join', 'outer', 'replace', 'with',
    'commit', 'rollback', 'current_date'
]


style = Style.from_dict(
    {
        "completion-menu.completion": "bg:#004444 #ffffff",
        "completion-menu.completion.current": "bg:#00aaaa #000000",
        "scrollbar.background": "bg:#88aaaa",
        "scrollbar.button": "bg:#222222",
    }
)


def main(root_dir=None):
    db = CSVDB(root_dir)
    populate_table_list(db)
    session = PromptSession(
        lexer=PygmentsLexer(SqlLexer),
        completer=WordCompleter(sql_csv_keywords, ignore_case=True),
        style=style,
        history=FileHistory('history.txt'),
        auto_suggest=AutoSuggestFromHistory()
    )

    while True:
        messages = []
        try:
            cmd = session.prompt("SQLCSV> ")
        except KeyboardInterrupt:
            continue  # Control-C pressed. Try again.
        except EOFError:
            break  # Control-D pressed.
        try:
            messages = execute_command(cmd, db)
            # add potential new table to the auto complete
            for table in db.table_list:
                if table.name not in sql_csv_keywords:
                    sql_csv_keywords.append(table.name)
        except Exception as e:
            print(repr(e))
        finally:
            for message in messages:
                print(message)


def execute_command(cmd, db):
    if cmd.strip() == '':
        return ['']
    cmd_list = cmd.split(' ')
    if cmd_list[0] == 'list':
        return db.get_table_name_list()
    if cmd_list[0] == 'list_changes':
        return db.print_modified_tables()
    if cmd_list[0] == 'desc':
        if cmd_list[1] is None:
            return ["desc require the table name as argument", "desc [file]"]
        return db.desc(cmd_list[1])
    if cmd_list[0] == 'load':
        if cmd_list[1] is None:
            return ["load require the path to the file or the directory as argument",
                    "load [directory|file]"]
        cmd_list[1] = cmd_list[1].replace('"', '')
        db.load(cmd_list[1])
        return []
    if cmd_list[0] == 'output':
        if cmd_list[1] is None:
            return ["output require the output format [pretty|csv|html]"]
        return db.set_output_format(cmd_list[1])
    if cmd_list[0] == 'spool':
        if cmd_list[1] is None:
            return ["spool command requires one argument", "spool [filename|off]"]
        return db.set_spool_file(cmd_list[1])
    if cmd_list[0] == 'help':
        return get_help_text()
    if cmd_list[0] == 'exit':
        sys.exit()
    else:
        return db.print_sql(cmd)


def populate_table_list(db):
    for table in db.table_list:
        if table.type != 'excel':
            if table.name not in sql_csv_keywords:
                sql_csv_keywords.append(table.name)
        for header in table.headers:
            if header not in sql_csv_keywords:
                sql_csv_keywords.append(header)


def get_help_text():
    return [
            " Usage interactive: ",
            "    sqlcsv ",
            "    sqlcsv [root_dir]",
            " Script Mode:",
            "    sqlcsv [root_dir] [sql_script]",
            "",
            " Commands:",
            "  load [file|directory]: load the file or the files in the directory",
            "                         into the database (csv, xls, xlsx)",
            "  list                 : give the list of tables loaded",
            "  commit_files         : additionally to commit in SQLLite,",
            "                         save the modifications in the csv or excel files",
            "  list_changes         : list modified tables",
            "                         commit_files would save changes to files",
            "  output               : switch output to pretty print, csv or html"
            "      [pretty|csv|html]  ",
            "  spool [file_name]    : switch the output to a file",
            "  desc [table_name]    : describe a table in SQLlite3",
            "  exit                 : quit the program",
            "  Ctrl-C               : clear prompt",
            "  Ctrl-D               : quit the program",
            "  arrows UP            : navigate though history",
            "  arrows RIGHT         : complete from history",
            "  arrows DOWN          : complete from dictionary",
            "  help                 : show this message"
            ]


def execute_script(root_dir, sql_script):
    db = CSVDB(root_dir)
    populate_table_list(db)
    script_file = open(sql_script, 'r')
    command = ''
    for line in script_file.readlines():
        command += line
        if line.strip().endswith(';'):
            print("Executing: " + command)
            execute_command(command, db)
            command = ''
    script_file.close()
    execute_command('exit', db)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', action='store', dest='root_dir', default=None, help='Root directory of the import')
    parser.add_argument('-f', action='store', dest='script_sql', default=None, help='SQLCSV script to apply')
    results = parser.parse_args()
    root_dir = results.root_dir
    sql_script = results.script_sql

    print("*** Welcome in SQLCSV 0.1")
    print("    An interactive prompt utils to manipulate csv and excel files through SQL")
    print("    Provide the SQLLite3 SQL set: https://www.sqlite.org/index.html")
    print("    help: provide the list of commands")

    if root_dir is not None:
        if sql_script is not None:
            # Script mode
            execute_script(root_dir, sql_script)
        else:
            # Interactive mode, load dir
            main(results.root_dir)
    else:
        # Interactive mode, load dir
        main()

