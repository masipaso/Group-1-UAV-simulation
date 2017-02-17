import os.path
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.autoreload

import webbrowser


class MainHandler(tornado.web.RequestHandler):
    """
    Handles the HTML template which holds the visualization
    """

    def get(self):
        self.render("index.html", port=self.application.port,
                    model_name=self.application.model_name,
                    includes=self.application.includes,
                    scripts=self.application.js_code)


class SocketHandler(tornado.websocket.WebSocketHandler):
    """
    Handles the Websocket connection
    """
    def open(self):
        print("Websocket open")

    def on_message(self, message):
        """
        When a message is received, parse it and act on the content
        :param message: A json message
        """
        msg = tornado.escape.json_decode(message)

        if msg["type"] == "get_step":
            self.application.model.step()
            message = {"type": "viz_state", "data": self.application.render_model()}
            self.write_message(message)
        elif msg["type"] == "reset":
            self.application.reset_model()
            message = {"type": "viz_state", "data": self.application.render_model()}
            self.write_message(message)
        elif msg["type"] == "get_details_for":
            pos = (msg["pos"]["x"], msg["pos"]["y"])
            details_for = self.application.model.get_details_for(pos)
            self.application.model.details_for = details_for
            message = {"type": "viz_state", "data": self.application.render_model()}
            self.write_message(message)

        else:
            if self.application.verbose:
                print("Unexpected message!")

    def check_origin(self, origin):
        return True


class VisualizationServer(tornado.web.Application):
    """
    VisualizationServer based on the VisualizationServer from MESA
    """
    port = 8521
    model_name = None
    model = None
    max_steps = 100000

    images_path = os.path.dirname(__file__) + "/images"
    styles_path = os.path.dirname(__file__) + "/styles"
    js_path = os.path.dirname(__file__) + "/js"
    modules_path = os.path.dirname(__file__) + "/modules"

    # Handlers
    main_handler = (r'/', MainHandler)
    socket_handler = (r'/ws', SocketHandler)
    image_handler = (r'/images/(.*)', tornado.web.StaticFileHandler, {"path": images_path})
    style_handler = (r'/styles/(.*)', tornado.web.StaticFileHandler, {"path": styles_path})
    js_handler = (r'/js/(.*)', tornado.web.StaticFileHandler, {"path": js_path})
    includes_handler = (r'/modules/(.*)', tornado.web.StaticFileHandler, {"path": modules_path})

    handlers = [main_handler, socket_handler, image_handler, style_handler, js_handler, includes_handler]

    settings = {
        "autoreload": False,
        "template_path": os.path.dirname(__file__) + "/templates"
    }

    def __init__(self, model_source, visualization_elements, name="No Name"):
        # Set all visualization elements
        self.visualization_elements = visualization_elements
        # Includes are only needed once
        self.includes = set()
        # JS code might be used multiple times
        self.js_code = []

        # Get all required includes for all elements
        for element in visualization_elements:
            for include in element.includes:
                self.includes.add(include)
            self.js_code.append(element.js_code)

        # Initializing the model
        self.model_name = name
        self.model_source = model_source
        self.reset_model()

        # Initializing the VisualizationServer
        super().__init__(self.handlers, **self.settings)

    def reset_model(self):
        """
        Reset the model
        """
        self.model = self.model_source()

    def render_model(self):
        """
        Transform the current state of the model into a dictionary of visualizations
        :return: a dictionary
        """
        visualization_state = []
        for element in self.visualization_elements:
            element_state = element.render(self.model)
            visualization_state.append(element_state)
        return visualization_state

    def launch(self, port=None):
        """
        Launch the server at localhost
        """
        start_loop = not tornado.ioloop.IOLoop.initialized()
        if port is not None:
            self.port = port
        url = 'http://localhost:{PORT}'.format(PORT=self.port)
        print('Interface starting at {url}'.format(url=url))
        self.listen(self.port)
        webbrowser.open(url)
        tornado.autoreload.start()
        if start_loop:
            tornado.ioloop.IOLoop.instance().start()
