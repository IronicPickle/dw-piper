# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['./duct.py'],
             pathex=['.'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += [("version", "./version", "Data")]
a.datas += Tree("./pdf_templates", prefix="pdf_templates")
a.datas += Tree("./images", prefix="images")

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Duct',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon="./images/icon.ico",
          manifest=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='duct')
