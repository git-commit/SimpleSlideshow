import sys
from cx_Freeze import setup, Executable



# GUI applications require a different base on Windows (the default is for a
# console application).
base = "Console"
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable(
        'Slideshow.py',
        base=base,
        )
]

# http://msdn.microsoft.com/en-us/library/windows/desktop/aa371847(v=vs.85).aspx
shortcut_table = [
    ("DesktopShortcut",            # Shortcut
     "DesktopFolder",              # Directory_
     "Slideshow",                  # Name
     "TARGETDIR",                  # Component_
     "[TARGETDIR]Slideshow.exe",   # Target
     "300",                         # Arguments
     None,                         # Description
     None,                         # Hotkey
     None,                         # Icon
     None,                         # IconIndex
     None,                         # ShowCmd
     'TARGETDIR'                   # WkDir
     ),
    ("StartMenuShortcut",            # Shortcut
     "StartMenuFolder",              # Directory_
     "Slideshow",                  # Name
     "TARGETDIR",                  # Component_
     "[TARGETDIR]Slideshow.exe",   # Target
     "300",                         # Arguments
     None,                         # Description
     None,                         # Hotkey
     None,                         # Icon
     None,                         # IconIndex
     None,                         # ShowCmd
     'TARGETDIR'                   # WkDir
     )

    ]

# Now create the table dictionary
msi_data = {"Shortcut": shortcut_table}

# Dependencies are automatically detected, but it might need
# fine tuning.
copyfiles = [
    ('C:\Python34\Lib\site-packages\PyQt5\libEGL.dll', 'libEGL.dll'),
    ]
build_exe_options = dict(packages=[], excludes=[], include_files=copyfiles)

bdist_msi_options = {
    "upgrade_code": "{183d99bc-6632-4235-8afc-c952da8639a3}",
    'data': msi_data
}


setup(name='Slideshow',
      version='0.2.1',
      description='Simple slideshow utility that shows all pictures in the current working directory',
      url='http://xerael.net',
      author='Maximilian Berger',

      options=dict(build_exe=build_exe_options,
                   bdist_msi=bdist_msi_options),
      executables=executables
      )
