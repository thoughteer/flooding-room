import pkg_resources

import flask


class App(flask.Flask):

    def __init__(self):
        flask.Flask.__init__(self, __name__)
        self.__configure()

    def __configure(self):

        @self.route("/")
        def index():
            return self.send_static_file("index.html")

        self.config["SECRET_KEY"] = "the secret"
        self.static_folder = pkg_resources.resource_filename("floodingroom", "server/resources")


app = App()
