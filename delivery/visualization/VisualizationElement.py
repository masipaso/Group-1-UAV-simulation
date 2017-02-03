class VisualizationElement:
    """
    Defines an element of the visualization.

    Attributes:
        includes: A list of JavaScript files that are local to the
                        directory that the server is being run in.
        js_code: A JavaScript code string to instantiate the element.

    Methods:
        render: Takes a model object, and produces JSON data which can be sent
                to the client.

    """

    includes = []
    js_code = ''

    def __init__(self):
        pass

    def render(self, model):
        """ Build visualization data from a model object.

        Args:
            model: A model object

        Returns:
            A JSON-ready object.

        """
        return "<b>VisualizationElement goes here</b>."