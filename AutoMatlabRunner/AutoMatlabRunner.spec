# -*- mode: python ; coding: utf-8 -*-

import os
import matlab

matlab_root = os.path.dirname(matlab.__file__)

a = Analysis(
    ['AutoMatlabRunner.py'],
    pathex=[],
    binaries=[],
    datas=[
        (matlab_root, 'matlab'),
    ],
    hiddenimports=['matlab', 'matlab.engine'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AutoMatlabRunner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
