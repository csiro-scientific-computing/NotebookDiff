import json

from tornado import gen, web

from notebook.utils import url_path_join
from jupyter_client.jsonutil import date_default

from notebook.base.handlers import (
    IPythonHandler, json_errors, path_regex,
)


class NotebookDiffHandler(IPythonHandler):
    
    SUPPORTED_METHODS = ('GET')
    
    @web.authenticated
    @json_errors
    @gen.coroutine
    def get(self, path='', commit='HEAD', path2=None):
        """runs nbdiff for a given notebook"""
        cm = self.contents_manager
        if path2:
            diff = yield gen.maybe_future(cm.file_diff(path, path2))
        else:
            diff = yield gen.maybe_future(cm.git_diff(path, commit))
        self.finish(diff)


class GitLogHandler(IPythonHandler):
    
    SUPPORTED_METHODS = ('GET')
    
    @web.authenticated
    @json_errors
    @gen.coroutine
    def get(self, path=''):
        """get the list of commits for a given notebook"""
        cm = self.contents_manager
        gitlog = yield gen.maybe_future(cm.git_log(path))
        data = json.dumps(gitlog, default=date_default)
        self.finish(data)


_checkpoint_id_regex = r"(?P<checkpoint_id>[\w-]+)"
_path2_regex = r"(?P<path2>(?:(?:/[^/]+)+|/?))"
_commit_regex = r"(?P<commit>[\w]{7})"

'''
default_handlers = [
    (r"/api/contents%s/gitlog" % path_regex, GitLogHandler),
    (r"/api/contents%s/nbdiff" % path_regex, NotebookDiffHandler),
    (r"/api/contents%s/nbdiff/%s" % (path_regex, _commit_regex), NotebookDiffHandler),
    (r"/api/contents%s/nbdiff%s" % (path_regex, _path2_regex), NotebookDiffHandler),
]
'''

def init_handlers(nbapp):
    webapp = nbapp.web_app
    base_url = webapp.settings['base_url']
    webapp.add_handlers(".*$", [
        (url_path_join(base_url, r"/api/contents%s/gitlog" % path_regex), GitLogHandler),
        (url_path_join(base_url, r"/api/contents%s/nbdiff" % path_regex), NotebookDiffHandler),
        (url_path_join(base_url, r"/api/contents%s/nbdiff/%s" % (path_regex, _commit_regex)), NotebookDiffHandler),
        (url_path_join(base_url, r"/api/contents%s/nbdiff%s" % (path_regex, _path2_regex)), NotebookDiffHandler),
    ])
