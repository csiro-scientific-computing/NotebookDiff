from setuptools import setup

setup(name='notebookdiff',
    version='0.1',
    description='Visual diff tool for Jupyter notebooks',
    url='https://github.com/csiro-scientific-computing/notebookdiff',
    author='Alex Kruger',
    author_email='Alex.Kruger@csiro.au',
    license='CSIRO BSD MIT',
    packages=['notebookdiff'],
    package_data = {'notebookdiff': ['*.tpl', 'notebookdiff_js/*.js']},
    install_requires = ['ipython>=3'],
    classifiers=['Development Status :: 4 - Beta'],
    zip_safe=False,
    )
