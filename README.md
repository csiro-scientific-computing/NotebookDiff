NotebookDiff
=======
This Jupyter extension can be used to visually compare a notebook to its previous versions in git from the notebook menu or to compare two different notebook files from the tree view.

Installation
------------
Install using pip
```
pip install https://github.com/csiro-scientific-computing/NotebookDiff/tarball/master
```

Add the following to `~/.ipython/profile_default/ipython_notebook_config.py`
```python
c.NotebookApp.contents_manager_class = 'notebookdiff.filemanager.NotebookDiffContentsManager'
c.NotebookApp.server_extensions = [ 'notebookdiff' ]
```

Add the following to `~/.ipython/profile_default/static/custom/custom.js`
```javascript
require([
    'base/js/events'
], function(events) {
    events.on('app_initialized.DashboardApp', function(){
        IPython.load_extensions('notebookdiff_js/tree_ui.js');
    });
});
```
