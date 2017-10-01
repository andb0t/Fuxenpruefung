# -*- mode: python -*-

block_cipher = None


a = Analysis(['fuxenpruefung.py'],
             pathex=[],
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
a.datas += [(r'images\fox.ico', r'src\images\fox.ico', 'DATA')]
a.datas += [(r'images\fox.png', r'src\images\fox.png', 'DATA')]
a.datas += [(r'images\floor.jpg', r'src\images\floor.jpg', 'DATA')]
a.datas += [(r'images\major.png', r'src\images\major.png', 'DATA')]
a.datas += [(r'images\bucket.png', r'src\images\bucket.png', 'DATA')]
a.datas += [(r'images\beer.png', r'src\images\beer.png', 'DATA')]
a.datas += [(r'images\star.png', r'src\images\star.png', 'DATA')]
a.datas += [(r'images\github.png', r'src\images\github.png', 'DATA')]
a.datas += [(r'images\ger_eng.png', r'src\images\ger_eng.png', 'DATA')]
a.datas += [(r'images\eng_bay.png', r'src\images\eng_bay.png', 'DATA')]
a.datas += [(r'images\bay_ger.png', r'src\images\bay_ger.png', 'DATA')]
a.datas += [(r'images\sound.png', r'src\images\sound.png', 'DATA')]
a.datas += [(r'images\mute.png', r'src\images\mute.png', 'DATA')]
a.datas += [(r'sounds\Ehr_unser_Zier.wav', r'src\sounds\Ehr_unser_Zier.wav', 'DATA')]
a.datas += [(r'sounds\Blop.wav', r'src\sounds\Blop.wav', 'DATA')]
a.datas += [(r'sounds\Slurp.wav', r'src\sounds\Slurp.wav', 'DATA')]
a.datas += [(r'sounds\Hiccup.wav', r'src\sounds\Hiccup.wav', 'DATA')]
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
