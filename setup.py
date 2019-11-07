from cx_Freeze import setup, Executable

base = None    

executables = [Executable("runthis.py", base=base)]

packages = ["idna","dns","email_validator",'lxml','requests','main',
            'filechunker','netScratcher','queue']
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "Email Validator Program ",
    options = options,
    version = "1.0",
    description = 'A Program to validate a list of 10k email list',
    executables = executables
)
