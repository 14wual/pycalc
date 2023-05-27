# pycalc.spec

import sys
from pathlib import Path

main_file = 'pycalc/__init__.py'

options = {
    'name': 'PyCalc',
    'noconsole': True,
    'onefile': True,
    'add_data': [
        (f'{Path().resolve()}/pycalc/src/images', 'pycalc/src/images'),
        (f'{Path().resolve()}/pycalc/src/log/history.csv', 'pycalc/src/log'),
        (f'{Path().resolve()}/pycalc/src/config.ini', 'pycalc/src'),
    ],
}

if sys.platform == 'win32':
    main_file = 'pycalc/windows.py'
elif sys.platform.startswith('linux'):
    main_file = 'pycalc/linux.py'

entry_point = Path(main_file).resolve()
a = Analysis([str(entry_point)], pathex=[str(entry_point.parent)], **options)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(pyz, a.scripts, a.binaries, a.zipfiles, a.datas, **options)
