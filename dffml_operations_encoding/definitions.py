import sys
from dffml.df.types import Definition

definitions = [
    Definition(name="filename", primitive="str"),
    Definition(name="base64_image", primitive="str"),
]

for definition in definitions:
    setattr(sys.modules[__name__], definition.name, definition)
