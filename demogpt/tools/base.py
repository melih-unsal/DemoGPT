

from langchain_core.tools import BaseTool as LangChainBaseTool
from typing import no_type_check

class BaseTool(LangChainBaseTool):
    def __init__(self, is_single_input=True):
        self.is_single_input = is_single_input
        self.setAttributes()
        
    def _run(self, *args, **kwargs):
        return None
    
    @no_type_check
    def __setattr__(self, name, value):  # noqa: C901 (ignore complexity)
        ...

    def setAttributes(self):

        for attribute in self.tool.__dict__:
            print(attribute)
            setattr(self, attribute, self.tool.__dict__[attribute])
    