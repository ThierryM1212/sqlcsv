<h1 align="center">Welcome to csvsql 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.1-blue.svg?cacheSeconds=2592000" />
  <a href="#" target="_blank">
    <img alt="License: lgplv3" src="https://img.shields.io/badge/License-lgplv3-yellow.svg" />
  </a>
</p>

> Interactive command line tool to manipulate csv and excel files through SQL
<br>[Download exe](https://github.com/ThierryM1212/sqlcsv/raw/master/dist/sqlcsv.exe)
<br>The tool allows you to load csv and/or excel files from a directory in an inmemory database (SQLlite3) and then manipulate the data using SQL.
<br>All SQLlite3 feature supported to update, join, aggregate the data.
<br>The commit of the modification update the csv/excel files.


## Usage

```sh
sqlcsv -d [root dir of csv/excel files]
```

## Run tests

```sh
sqlcsv -d test/data
```

## Build exe

```sh
pyinstaller sqlcsv.spec
```

## Interactive mode help

```sh
Usage interactive: 
   sqlcsv 
   sqlcsv [root_dir]
Script Mode:
   sqlcsv [root_dir] [sql_script]

Commands:
 load [file|directory]: load the file or the files in the directory
                        into the database (csv, xls, xlsx)
 list                 : give the list of tables loaded
 commit_files         : additionally to commit in SQLLite,
                        save the modifications in the csv or excel files
 list_changes         : list modified tables
                        commit_files would save changes to files
 output               : switch output to pretty print, csv or html
     [pretty|csv|html]
 spool [file_name]    : switch the output to a file
 desc [table_name]    : describe a table in SQLlite3
 exit                 : quit the program
 Ctrl-C               : clear prompt
 Ctrl-D               : quit the program
 arrows UP            : navigate though history
 arrows RIGHT         : complete from history
 arrows DOWN          : complete from dictionary
 help                 : show this message
```

## Author

👤 **Thierry.M**

* Github: [@thierry.m](https://github.com/thierry.m)

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
