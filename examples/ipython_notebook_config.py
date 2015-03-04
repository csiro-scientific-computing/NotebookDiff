# Configuration file for ipython-notebook.

c = get_config()

c.NotebookApp.contents_manager_class = 'notebookdiff.filemanager.NotebookDiffContentsManager'
c.NotebookApp.server_extensions = [ 'notebookdiff' ]