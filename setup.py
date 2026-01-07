"""Sets up the parameters required by PyPI"""
from pathlib import Path
from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

setup(
    name='mkdocs-alias-plugin',
    version='0.10.0',
    description=
    'An MkDocs plugin allowing links to your pages using a custom alias',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='mkdocs python markdown alias link wiki',
    url='https://github.com/eddyluten/mkdocs-alias-plugin',
    author='Eddy Luten',
    author_email='eddyluten@gmail.com',
    license='MIT',
    python_requires='>=3.0',
    install_requires=['mkdocs', 'markdown'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Topic :: Documentation",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Markup",
        "Topic :: Text Processing :: Markup :: Markdown",
    ],
    packages=find_packages(exclude=['*.tests']),
    entry_points={
        'mkdocs.plugins': ['alias = alias.plugin:AliasPlugin']
    })
