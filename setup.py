import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='mkdocs-alias-plugin',
    version='0.1.0',
    description=
    'An MkDocs plugin allowing links to your pages using a custom alias',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    keywords='mkdocs python markdown alias link wiki',
    url='https://github.com/eddyluten/mkdocs-alias-plugin',
    author='Eddy Luten',
    author_email='eddyluten@gmail.com',
    license='MIT',
    python_requires='>=3.0',
    install_requires=['mkdocs'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(exclude=['*.tests']),
    entry_points={
        'mkdocs.plugins': ['alias = alias.plugin:AliasPlugin']
    })
