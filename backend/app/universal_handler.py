import json
from functools import wraps
from . import request, g, Response


class UniversalHandler:
    """
    Class works as a replacement for the default app.route decorator. Instantiated as follows:
    >>> Handler = UniversalHandler(your_flask_app)
    """
    def __init__(self, target):
        self._target = target

    def __call__(self, route, methods):
        """
        The __call__ function is a decorator generator. This method is mostly just black magic, so do not question it.
        Sample usage:
        >>> @Handler('/', methods=['GET'])
        >>> def index_endpoint():
        >>>     return Response("lalala", status=200)
        :param f: The function that is decorated by an instance of the Handler class.
        :return: A decorator for preprocessing and postprocessing data going in and out of view functions.
        """
        def decorator(f):
            """
            Decorator wraps the view function and adds it as a path to the flask app.
            :param f: The view function
            :return: A decorator
            """
            @wraps(f)
            def argument_grabbing_wrapper(*args, **kwargs):
                """
                Method captures the arguments passed to the view function and can preprocess them if necessary.
                Method also postprocesses the response out of the view function.

                Method calls the view function and converts the output to a Flask Response. For every type, these
                conversions happen:

                int -> Becomes the status code of an empty Response
                list or dict -> dumped as JSON and returned with appropriate headers
                Response -> Stays the same
                otherwise -> cast to string and made into a Response

                :param args:
                :param kwargs:
                :return: A flask Response
                """

                # TODO: Add input argument validation
                res = f(*args, **kwargs)

                if type(res) in (dict, list):
                    res = Response(json.dumps(res), status=200, headers={"Content-Type": "application/json"})
                elif type(res) is int:
                    res = Response(status=res)
                elif not isinstance(res, Response):
                    res = Response(str(res), status=200)

                return res
            self._target.add_url_rule(route, methods=methods, view_func=argument_grabbing_wrapper)
            return argument_grabbing_wrapper
        return decorator


