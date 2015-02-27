NotebookDiff
=======

Requirements:
-------------
    IPython 3 or greater

Installation (from repository):
------------------------------
    python setup.py install
    python install.py
    c.NotebookApp.server_extensions = [ 'notebookdiff' ]
    c.NotebookApp.contents_manager_class = 'notebookdiff.filemanager.NotebookDiffContentsManager'
