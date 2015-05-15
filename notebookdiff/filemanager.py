import io
import os

from IPython.html.services.contents.filemanager import FileContentsManager

from IPython.utils.encoding import DEFAULT_ENCODING
import subprocess

from . import notebook_diff

class NotebookDiffContentsManager(FileContentsManager):        
    def __init__(self, *args, **kwargs):
        # Install the nbextension when instantiated
        from os.path import dirname, abspath, join as pjoin
        from IPython.html.nbextensions import install_nbextension
        from IPython.html.services.config import ConfigManager

        # Install the extension
        notebookdiffdir = pjoin(dirname(abspath(__file__)), 'notebookdiff_js')
        install_nbextension(notebookdiffdir, user=True)

        # Enable the extension
        cm = ConfigManager()
        cm.update('notebook', {"load_extensions": {"notebookdiff_js/notebook_ui": True}})

        # call the parent constructor
        super(NotebookDiffContentsManager, self).__init__(*args, **kwargs)


    def git_log(self, path):
        path = path.strip(os.sep)
        path = self._get_os_path(path)
        list = []
        if os.path.isfile(path):
            try:
                dir = path.rsplit(os.sep, 1)[0]
                cmd = subprocess.Popen(
                    ['git', 'log', '--pretty=format:"%h - %cd"', path],
                    cwd=dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT
                )
                output = cmd.communicate()[0].decode(DEFAULT_ENCODING, 'replace')
                for commit in output.splitlines():
                    commitinfo = commit.strip('"').split('-')
                    if len(commitinfo) == 2:
                        cp = dict(
                            id=commitinfo[0].strip(),
                            last_modified=commitinfo[1].strip()
                        )
                        list.append(cp)
            except subprocess.CalledProcessError as e:
                if e.returncode == 128:
                    #file not committed
                    pass
                else:
                    err = e.output.decode(DEFAULT_ENCODING, 'replace')
                    self.log.exception(err)
            except (FileNotFoundError, IOError):
                #git not installed
                pass
        return list
        
    def git_diff(self, path='', commit='HEAD'):
        html = 'Internal Server Error has occured'
        path = path.strip(os.sep)
        nbpath = self._get_os_path(path)
        if os.path.isfile(nbpath): 
            try:
                #check if file is in git
                dir = nbpath.rsplit(os.sep, 1)[0]
                cmd = subprocess.Popen(
                    ['git', 'log', '--pretty=format:"%h - %cd"', nbpath],
                    cwd=dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT
                )
                if len(cmd.communicate()[0].decode(DEFAULT_ENCODING, 'replace')) > 0:
                    right = notebook_diff.NBDiff.readnb(open(nbpath))
                    name = nbpath.rsplit(os.sep, 1)[-1]
                    left = notebook_diff.NBDiff.readjson(subprocess.Popen(
                        ['git', 'show', '%s:./%s' % (commit, name)],
                        cwd=dir,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT
                    ).communicate()[0].decode(DEFAULT_ENCODING, 'replace'))
                    nbnode = notebook_diff.NBDiff.notebook_diff(left, right, self.log)
                    leftname = name + " (" + commit + ")"
                    diffexporter = notebook_diff.Exporter()
                    output, resources = diffexporter.from_notebook_node(nbnode, resources={
                        'left':{'name':leftname},
                        'right':{'name':name}
                    })
                    html = output
                else:
                    html = 'This notebook has not been commited into git'
            except subprocess.CalledProcessError as e:
                if e.returncode == 128:
                    html = 'This notebook has not been commited into git'
                else:
                    err = e.output.decode(DEFAULT_ENCODING, 'replace')
                    self.log.exception(err)
            #except (FileNotFoundError, IOError):
            #    html = 'Git is not installed'
        return html
        
    def file_diff(self, path='', path2=''):
        html = 'Internal Server Error has occured'
        path = path.strip(os.sep)
        path2 = path2.strip(os.sep)
        nbpath = self._get_os_path(path)
        nbpath2 = self._get_os_path(path2)
        if os.path.isfile(nbpath) and os.path.isfile(nbpath2): 
            right = notebook_diff.NBDiff.readnb(open(nbpath))
            left = notebook_diff.NBDiff.readnb(open(nbpath2))
            nbnode = notebook_diff.NBDiff.notebook_diff(left, right, self.log)
            rightname = nbpath.rsplit(os.sep, 1)[-1]
            leftname = nbpath2.rsplit(os.sep, 1)[-1]
            diffexporter = notebook_diff.Exporter()
            output, resources = diffexporter.from_notebook_node(nbnode, resources={
                'left':{'name':leftname},
                'right':{'name':rightname}
            })
            html = output
        return html
