import sys
import tempfile

from dffml.df.types import Input
from dffml.df.base import operation_in, opimp_in, Operation
from dffml.df.memory import MemoryOrchestrator
from dffml.operation.output import GetSingle
from dffml.util.asynctestcase import AsyncTestCase

from dffml_operations_encoding.operations import *

OPIMPS = opimp_in(sys.modules[__name__])

TEST_IMAGE = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x02\x08\x02\x00\x00\x00\xfd\xd4\x9as\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x07tIME\x07\xe3\x07\x1d\x148#\xe2\x80V\xfb\x00\x00\x00\x1diTXtComment\x00\x00\x00\x00\x00Created with GIMPd.e\x07\x00\x00\x00\x12IDAT\x08\xd7c\xf8\xff\xff?\x03\x04\xfc\xff\xff\x1f\x00)\xe4\x05\xfb{\x0eb\x08\x00\x00\x00\x00IEND\xaeB`\x82"
TEST_IMAGE_CORRECT = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4wcdFDgj4oBW+wAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUHAAAAEklEQVQI12P4//8/AwT8//8fACnkBft7DmIIAAAAAElFTkSuQmCC"


class TestOperations(AsyncTestCase):
    async def test_run(self):

        with tempfile.NamedTemporaryFile(suffix=".png") as fileobj:
            async with MemoryOrchestrator.basic_config(
                *OPIMPS
            ) as orchestrator:
                fileobj.write(TEST_IMAGE)
                fileobj.seek(0)

                check = {fileobj.name: TEST_IMAGE_CORRECT}

                async with orchestrator() as octx:
                    for input_value in check.keys():
                        await octx.ictx.sadd(
                            input_value,
                            Input(
                                value=input_value,
                                definition=encode_base64_image.op.inputs[
                                    "filename"
                                ],
                            ),
                            Input(
                                value=[
                                    encode_base64_image.op.outputs[
                                        "base64_image"
                                    ].name
                                ],
                                definition=GetSingle.op.inputs["spec"],
                            ),
                        )

                    async for ctx, results in octx.run_operations(strict=True):
                        ctx_str = (await ctx.handle()).as_string()
                        self.assertEqual(
                            check[ctx_str],
                            results[GetSingle.op.name][
                                encode_base64_image.op.outputs[
                                    "base64_image"
                                ].name
                            ],
                        )
