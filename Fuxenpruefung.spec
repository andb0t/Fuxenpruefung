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
a.datas += [('fox.ico', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\fox.ico', 'DATA')]
a.datas += [('fox.png', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\fox.png', 'DATA')]
a.datas += [('github.png', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\github.png', 'DATA')]
a.datas += [('language.png', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\language.png', 'DATA')]
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Fuxenpruefung',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='fox.ico')
