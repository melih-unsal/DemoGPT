human_template = """
variable: url
instruction: Get website URL from the user
placeholder:Enter website URL

variable: source_text
instruction: Get source text from the user
placeholder:Type the source text

variable: input_language
instruction: Get the input language from the user
placeholder:Enter the input language

variable: {variable}
instruction: {instruction}
placeholder:

"""
