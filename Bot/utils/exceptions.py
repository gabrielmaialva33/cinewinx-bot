class AssistantErr(Exception):
    def __init__(self, err: str):
        super().__init__(err)
