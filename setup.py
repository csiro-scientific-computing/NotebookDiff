from __future__ import print_function
from setuptools import setup
import sys

def fail(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)
    
def main():
    try:
        import IPython
        if IPython.version_info[0] < 3:
            fail("NotebookDiff requires IPython 3.0 or greater.")
    except ImportError:
        fail("NotebookDiff requires IPython.")
    
    setup(name='notebookdiff',
        version='0.1',
        description='Visual diff tool for IPython notebooks',
        url='https://github.com/csiro-scientific-computing/notebookdiff',
        author='Alex Kruger',
        author_email='Alex.Kruger@csiro.au',
        license='CSIRO BSD MIT',
        packages=['notebookdiff'],
        classifiers=['Development Status :: 4 - Beta'],
        data_files=[('notebookdiff', ['notebookdiff/nbdiff.tpl'])],
        zip_safe=False)

if __name__ == '__main__':
    main()