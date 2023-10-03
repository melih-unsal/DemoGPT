import json
from pprint import pprint

from demogpt.chains.chains import Chains

Chains.setLlm("gpt-3.5-turbo")

instruction = "Create an app that can say the number of columns, rows, the name of columns from csv file"
res = Chains.appType(instruction=instruction)
pprint(res)
