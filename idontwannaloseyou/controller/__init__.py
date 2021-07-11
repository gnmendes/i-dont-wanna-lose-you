from enum import Enum, auto


class Verbs(Enum):
    POST = auto()
    GET = auto()
    PUT = auto()
    DELETE = auto()
    PATCH = auto()

    def __str__(self):
        return str(self.name)


from flask import Flask

app = Flask(__name__)

import idontwannaloseyou.controller.video_controller

