from cx_Freeze import setup, Executable
base = None
executables = [Executable("sqlcsv.py", base=base)]
packages = ["chardet","cx_Freeze","idna","numpy","pandas","pip","prettytable","prompt_toolkit",
            "dateutil","pytz","setuptools","six","wcwidth","pygments"]
options = {
    'build_exe': {
        'packages':packages,
    },
}
setup(
    name="sqlcsv",
    options=options,
    version="0.1",
    description='CLI to access and modify set of csv files through SQL',
    executables=executables
)
