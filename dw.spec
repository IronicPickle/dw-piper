# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['./dw.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += [("icon.ico", "./icon.ico", "Data")]
a.datas += [("version", "./version", "Data")]
a.datas += Tree("./pdf_templates", prefix="pdf_templates")
a.datas += Tree("./images", prefix="images")

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='DW-Piper',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon="./icon.ico",
          manifest=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='dw')
