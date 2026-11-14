class InputFileNotExists(Exception):
    """Exception raised when the program expects an input file to exist"""
    def __init__(self, message, path):
        super().__init__(message)
        self.message = message
        self.path = path

    def __str__(self):
        return f"{self.message} ({self.path})"

class InputFileUnexpectedFormat(Exception):
    """Exception raised when the program expects a different input file format"""
    def __init__(self, message, path):
        super().__init__(message)
        self.message = message
        self.path = path

    def __str__(self):
        return f"{self.message} ({self.path})"