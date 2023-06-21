class RequestClass:
    """ Class that represents the request to server """
    def __init__(self, type: str, file_names: list[str]):
        self.type = type
        self.file_names = file_names