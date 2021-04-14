# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
debug = False
upx = True

duct_a = Analysis(
  ['./duct.py'], pathex=['.'], hiddenimports=[], hookspath=None
)
duct_a.datas += [("version", "./version", "Data")]
duct_a.datas += Tree("./pdf_templates", prefix="pdf_templates")
duct_a.datas += Tree("./images", prefix="images")

background_a = Analysis(
  ['./background.py'], pathex=['.'], hiddenimports=[], hookspath=None
)
background_a.datas += [("version", "./version", "Data")]
background_a.datas += Tree("./images", prefix="images")

MERGE( (duct_a, "duct_a", "duct_a"), (background_a, "background_a", "background_a") )

duct_pyz = PYZ(duct_a.pure, duct_a.zipped_data, cipher=block_cipher)
duct_exe = EXE(
  duct_pyz, duct_a.scripts, [], exclude_binaries=True, name='Duct', debug=debug,
  console=debug, icon="./images/icon.ico", manifest=None, upx=upx
)
duct_coll = COLLECT(
  duct_exe, duct_a.binaries, duct_a.zipfiles, duct_a.datas, name='duct', upx=upx
)

background_pyz = PYZ(background_a.pure, background_a.zipped_data, cipher=block_cipher)
background_exe = EXE(
  background_pyz, background_a.scripts, [], exclude_binaries=True, name='Duct Background', debug=debug,
  console=debug, icon="./images/icon.ico", manifest=None, upx=upx
)
background_coll = COLLECT(
  background_exe, background_a.binaries, background_a.zipfiles, background_a.datas, name='duct_background', upx=upx
)
