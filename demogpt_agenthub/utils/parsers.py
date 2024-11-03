from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import BaseOutputParser


# The [bool] desribes a parameterization of a generic.
# It's basically indicating what the return type of parse is
# in this case the return type is either True or False
class BooleanOutputParser(BaseOutputParser[bool]):
    """Custom boolean parser."""

    true_val: str = "<YES>"
    false_val: str = "<NO>"

    def parse(self, text: str) -> bool:
        cleaned_text = text.strip().upper()
        if self.true_val.upper() in cleaned_text:
            return True
        elif self.false_val.upper() in cleaned_text:
            return False
        else:
            raise OutputParserException(
                f"BooleanOutputParser expected output value to either be "
                f"{self.true_val} or {self.false_val} (case-insensitive). "
                f"Received {cleaned_text}."
            )

    @property
    def _type(self) -> str:
        return "boolean_output_parser"