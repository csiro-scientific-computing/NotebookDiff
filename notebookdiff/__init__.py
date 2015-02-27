from . import handlers

def load_jupyter_server_extension(nbapp):
    handlers.init_handlers(nbapp)