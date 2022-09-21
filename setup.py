from setuptools import find_packages, setup

'''
The setup.py file describes your project and the files that belong to it.
packages tells Python what package directories (and the Python files they contain) to include. 
find_packages() finds these directories automatically so you don’t have to type them out. 
To include other files, such as the static and templates directories, include_package_data is set. 
Python needs another file named MANIFEST.in to tell what this other data is.

The manifest file tells Python to copy everything in the static and templates directories, 
and the schema.sql file, but to exclude all bytecode files.
'''
setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
