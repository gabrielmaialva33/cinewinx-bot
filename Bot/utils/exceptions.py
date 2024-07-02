class AssistantErr(Exception):
    def __init__(self, err: str | Exception):
        super().__init__(err)
