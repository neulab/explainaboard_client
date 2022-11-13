class APIVersionMismatchException(Exception):
    def __init__(self, message, package, required_version, current_version):
        super().__init__(message)
        self.message = message
        self.package = package
        self.required_version = required_version
        self.current_version = current_version
