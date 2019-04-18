import cherrypy

from landlab_rest import create_app

app = create_app()


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=80, help="port to run on")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="host IP address")

    args = parser.parse_args()

    # Mount the application
    cherrypy.tree.graft(app, "/")

    # Unsubscribe the default server
    cherrypy.server.unsubscribe()

    # Instantiate a new server object
    server = cherrypy._cpserver.Server()

    # Configure the server object
    server.socket_host = args.host
    server.socket_port = args.port
    server.thread_pool = 30

    # For SSL Support
    # server.ssl_module            = 'pyopenssl'
    # server.ssl_certificate       = 'ssl/certificate.crt'
    # server.ssl_private_key       = 'ssl/private.key'
    # server.ssl_certificate_chain = 'ssl/bundle.crt'

    # Subscribe this server
    server.subscribe()

    # Start the server engine (Option 1 *and* 2)

    cherrypy.engine.start()
    cherrypy.engine.block()
