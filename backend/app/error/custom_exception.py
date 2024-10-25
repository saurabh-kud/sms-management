class CustomException(Exception):
    def __init__(
        self,
        message: str = "Oops! Something went wrong. Please try again later.",
        status: int = 500,
    ) -> None:
        self.message = message
        self.status = status
        super().__init__(self.message, self.status)