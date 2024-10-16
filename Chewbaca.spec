# Chewbaca.spec

block_cipher = None

a = Analysis(
    ['scripts/v6_main.py'],  # Your script path
    pathex=['.'],  # Ensure your working directory is included
    binaries=[],
    datas=[
        ('docs/parsed_chewbaca.jsonl', '_internal/docs'),
        ('docs/ssms new query.png', '_internal/docs'),
        ('docs/ssms server name.png', '_internal/docs')
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Chewbaca',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Change to True if you want a console window for debugging
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='Chewbaca'
)
