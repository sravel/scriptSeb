
# -*- mode: python -*-

block_cipher = None

added_files = [ ('includes/*', 'includes'), ]

a = Analysis(['GUI_EBimage5.py'],
             pathex=['/media/sebastien/Bayer/ScriptsSEB/scripts/GUI/EBimage/'],
             binaries=None,
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='GUI_EBimage5_linux',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='includes/icon.ico', resources=['EBimage.ui'])


