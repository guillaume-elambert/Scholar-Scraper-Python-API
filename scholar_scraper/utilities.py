from json import JSONEncoder


def getObjectPublicAttributes(obj):
    """
    Get all the public attributes of an object.
    :param obj: The object to get the attributes from.
    :return: The dictionary of the public attributes.
    """
    return [attr for attr in dir(obj.__class__) if
            not callable(getattr(obj.__class__, attr))
            and not attr.startswith("__")
            and not attr.startswith("_")
            and not attr.startswith("_" + obj.__class__.__name__ + "__")]


class JSONEncoder(JSONEncoder):
    """
    Simple JSON encoder class that allows to serialize objects that are not serializable by default.
    """

    def default(self, o):
        """
        Returns the object's dictionary if it has one But only the attributes that are returned by the
        :meth:`getObjectPublicAttributes` function.
        :param o: The object to serialize
        :return: The object's dictionary
        """
        if not hasattr(o, '__dict__'):
            return JSONEncoder.default(self, o)

        if hasattr(o, '_class_attributes'):
            return {k: v for k, v in o.__dict__.items() if k in o._class_attributes}

        return {k: v for k, v in o.__dict__.items() if k in getObjectPublicAttributes(o)}
