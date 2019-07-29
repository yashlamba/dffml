import base64
import mimetypes
from pathlib import Path

from dffml.df.base import op

from .definitions import filename, base64_image


@op(inputs={"filename": filename}, outputs={"base64_image": base64_image})
async def encode_base64_image(filename: str):
    mimetype = mimetypes.guess_type(filename)[0]
    data = base64.b64encode(Path(filename).read_bytes()).decode()
    return {"base64_image": f"data:{mimetype};base64,{data}"}
