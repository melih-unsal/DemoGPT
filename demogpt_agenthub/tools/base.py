class BaseTool:
    def __init__(self, **data):
        super().__init__(**data)
        self.setAttributes()

    def setAttributes(self):
        if hasattr(self, 'tool') and self.tool:
            for attribute in self.tool.__dict__:
                setattr(self, attribute, self.tool.__dict__[attribute])