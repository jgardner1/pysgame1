# -*- mode: python -*-
a = Analysis(['.\\play.pyw'],
             pathex=['D:\\Documents\\GitHub\\pysgame1'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

a.datas += [(filename, a.pathex[0]+'\\data\\'+filename, 'DATA') for filename in (
	'female_names.txt',
	'male_names.txt',
	'surnames.txt')]

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='pysgame1.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
