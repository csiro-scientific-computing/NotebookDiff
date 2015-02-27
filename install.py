from os.path import dirname, abspath, join as pjoin
from IPython.html.nbextensions import install_nbextension
from IPython.html.services.config import ConfigManager

print("Installing nbextension ...")
notebookdiffdir = pjoin(dirname(abspath(__file__)), 'notebookdiff_js')
install_nbextension(notebookdiffdir, user=True)

print("Enabling the extension ...")
cm = ConfigManager()
cm.update('notebook', {"load_extensions": {"notebookdiff_js/notebookdiff_ui": True}})

print("Done.")