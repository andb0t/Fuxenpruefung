# -*- mode: python -*-

block_cipher = None


a = Analysis(['fuxenpruefung.py'],
             pathex=['C:\\Users\\Andreas Maier\\Dropbox\\Projects\\Python\\Fuxenpruefung'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
a.datas += [(r'images\fox.ico', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\src\images\fox.ico', 'DATA')]
a.datas += [(r'images\fox.png', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\src\images\fox.png', 'DATA')]
a.datas += [(r'images\github.png', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\src\images\github.png', 'DATA')]
a.datas += [(r'images\ger_eng.png', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\src\images\ger_eng.png', 'DATA')]
a.datas += [(r'images\eng_bay.png', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\src\images\eng_bay.png', 'DATA')]
a.datas += [(r'images\bay_ger.png', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\src\images\bay_ger.png', 'DATA')]
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='fuxenpruefung',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon=r'src\images\fox.ico')
