# -*- mode: python ; coding: utf-8 -*-
import sys
import os

python_dll = os.path.join(sys.base_prefix, f'python{sys.version_info.major}{sys.version_info.minor}.dll')

a = Analysis(
    ['src/desctop_app/app.py'],
    pathex=[],
    binaries=[
        (python_dll, '.'),  
    ],
    datas=[
        ('src/desctop_app/languages', 'languages'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Cryptall_2',
)
