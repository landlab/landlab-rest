import cherrypy
from landlab_rest import create_app

app = create_app()


def start(host, port, ssl_cert, ssl_key, ssl_chain):

    # Mount the application
    cherrypy.tree.graft(app, "/")

    # Unsubscribe the default server
    cherrypy.server.unsubscribe()

    # Instantiate a new server object
    server = cherrypy._cpserver.Server()

    # Configure the server object
    server.socket_host = host
    server.socket_port = port
    server.thread_pool = 30

    # For SSL Support
    if ssl_cert is not None and ssl_key is not None:
        server.ssl_module            = 'builtin'
        server.ssl_certificate       = ssl_cert
        server.ssl_private_key       = ssl_key
        server.ssl_certificate_chain = ssl_chain

    # Subscribe this server
    server.subscribe()

    # Start the server engine (Option 1 *and* 2)

    cherrypy.engine.start()
    cherrypy.engine.block()
