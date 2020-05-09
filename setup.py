from cx_Freeze import setup, Executable

buildOptions = {
    'include_files': ['config/', 'data/'],
    'includes': ['sounddevice', 'soundfile', 'pygame', 're', 'pathlib', 'logging', 'random'],
    'packages': ['PyPhone']
}

setup(
    name='A la recherche de la verite',
    version='1.0',
    description='Application telephone fictif projet mas drevon',
    author='Shyzuna',
    options={
        'build_exe': buildOptions
    },
    executables=[Executable('main.py')]
)