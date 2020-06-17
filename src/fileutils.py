import os
import re
import time
from pathlib import Path

CSV_REG_LIST = ["*.[cC][sS][vV]"]
XL_REG_LIST = ["*.[xX][lL][sS]", "*.[xX][lL][sS][xX]"]


def get_all_supported_files(root_dir):
    return {
        'csv': get_csv_list(root_dir),
        'excel': get_excel_list(root_dir)
    }


def get_csv_list(root_dir):
    return get_file_list(root_dir, CSV_REG_LIST)


def get_excel_list(root_dir):
    excel_list = get_file_list(root_dir, XL_REG_LIST)
    result = []
    for file in excel_list:
        if "~" not in str(file):
            result.append(file)
    return result


def get_file_list(root_dir, patterns):
    table_list = []
    result = []
    for pattern in patterns:
        result += list(Path(root_dir).rglob(pattern))
    for file in result:
        if os.path.getsize(file) > 0:
            table_list.append(file)
    return table_list


def compute_table_name(file_path, root_dir):
    if root_dir != '':
        # remove the root_dir from path
        name = os.path.relpath(file_path, root_dir)
    else:
        name = os.path.basename(file_path)

    # remove csv extension
    name = os.path.splitext(name)[0]
    # replace special char
    name = re.sub('[^0-9a-zA-Z]+', '_', name)
    return name


def get_file_type(filepath):
    ext = os.path.splitext(filepath)[1]
    if ext.lower() == '.csv':
        return 'csv'
    if ext.lower() in ['.xls', '.xlsx']:
        return 'excel'
    else:
        return None


def get_backup_file(filepath):
    return str(filepath) + "." + time.strftime("%Y%m%d_%H%M%S") + '.bak'


def make_html_page(html_table):
    return """<html>
<head>
<style>
table a:link {
	color: #666;
	font-weight: bold;
	text-decoration:none;
}
table a:visited {
	color: #999999;
	font-weight:bold;
	text-decoration:none;
}
table a:active,
table a:hover {
	color: #bd5a35;
	text-decoration:underline;
}
table {
	font-family:Arial, Helvetica, sans-serif;
	color:#666;
	font-size:12px;
	text-shadow: 1px 1px 0px #fff;
	background:#eaebec;
	margin:20px;
	border:#ccc 1px solid;

	-moz-border-radius:3px;
	-webkit-border-radius:3px;
	border-radius:3px;

	-moz-box-shadow: 0 1px 2px #d1d1d1;
	-webkit-box-shadow: 0 1px 2px #d1d1d1;
	box-shadow: 0 1px 2px #d1d1d1;
}
table th {
	padding:21px 25px 22px 25px;
	border-top:1px solid #fafafa;
	border-bottom:1px solid #e0e0e0;

	background: #ededed;
	background: -webkit-gradient(linear, left top, left bottom, from(#ededed), to(#ebebeb));
	background: -moz-linear-gradient(top,  #ededed,  #ebebeb);
}
table th:first-child {
	text-align: left;
	padding-left:20px;
}
table tr:first-child th:first-child {
	-moz-border-radius-topleft:3px;
	-webkit-border-top-left-radius:3px;
	border-top-left-radius:3px;
}
table tr:first-child th:last-child {
	-moz-border-radius-topright:3px;
	-webkit-border-top-right-radius:3px;
	border-top-right-radius:3px;
}
table tr {
	text-align: center;
	padding-left:20px;
}
table td:first-child {
	text-align: left;
	padding-left:20px;
	border-left: 0;
}
table td {
	padding:18px;
	border-top: 1px solid #ffffff;
	border-bottom:1px solid #e0e0e0;
	border-left: 1px solid #e0e0e0;

	background: #fafafa;
	background: -webkit-gradient(linear, left top, left bottom, from(#fbfbfb), to(#fafafa));
	background: -moz-linear-gradient(top,  #fbfbfb,  #fafafa);
}
table tr.even td {
	background: #f6f6f6;
	background: -webkit-gradient(linear, left top, left bottom, from(#f8f8f8), to(#f6f6f6));
	background: -moz-linear-gradient(top,  #f8f8f8,  #f6f6f6);
}
table tr:last-child td {
	border-bottom:0;
}
table tr:last-child td:first-child {
	-moz-border-radius-bottomleft:3px;
	-webkit-border-bottom-left-radius:3px;
	border-bottom-left-radius:3px;
}
table tr:last-child td:last-child {
	-moz-border-radius-bottomright:3px;
	-webkit-border-bottom-right-radius:3px;
	border-bottom-right-radius:3px;
}
table tr:hover td {
	background: #f2f2f2;
	background: -webkit-gradient(linear, left top, left bottom, from(#f2f2f2), to(#f0f0f0));
	background: -moz-linear-gradient(top,  #f2f2f2,  #f0f0f0);	
}
</style>
</head>
<body>
%s
</body>
</html>
""" % html_table
