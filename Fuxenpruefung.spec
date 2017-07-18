# -*- mode: python -*-

block_cipher = None


a = Analysis(['Fuxenpruefung.py'],
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
a.datas += [(r'Images\fox.ico', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\Images\fox.ico', 'DATA')]
a.datas += [(r'Images\fox.png', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\Images\fox.png', 'DATA')]
a.datas += [(r'Images\github.png', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\Images\github.png', 'DATA')]
a.datas += [(r'Images\language.png', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\Images\language.png', 'DATA')]
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Fuxenpruefung',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon=r'Images\fox.ico')
