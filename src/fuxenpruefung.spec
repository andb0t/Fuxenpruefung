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
a.datas += [(r'images\beer.png', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\src\images\beer.png', 'DATA')]
a.datas += [(r'images\star.png', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\src\images\star.png', 'DATA')]
a.datas += [(r'images\github.png', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\src\images\github.png', 'DATA')]
a.datas += [(r'images\ger_eng.png', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\src\images\ger_eng.png', 'DATA')]
a.datas += [(r'images\eng_bay.png', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\src\images\eng_bay.png', 'DATA')]
a.datas += [(r'images\bay_ger.png', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\src\images\bay_ger.png', 'DATA')]
a.datas += [(r'images\sound.png', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\src\images\sound.png', 'DATA')]
a.datas += [(r'images\mute.png', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\src\images\mute.png', 'DATA')]
a.datas += [(r'sounds\Ehr_unser_Zier.wav', r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\src\sounds\Ehr_unser_Zier.wav', 'DATA')]
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
