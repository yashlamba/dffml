# DFFML Encoding Operations

Encoding and decoding related operations

## Usage

Example usage

```console
export OPIMPS="encode_base64_image get_single"
dffml operations repo \
  -keys ~/Pictures/test_2x2.png \
  -sources mydataset=json \
  -source-filename mydataset.json \
  -repo-def filename \
  -dff-memory-operation-network-ops $OPIMPS \
  -dff-memory-opimp-network-opimps $OPIMPS \
  -output-specs '["base64_image"]=get_single_spec' \
  -remap get_single.base64_image=base64_image \
  -log debug \
  -update
```

## License

DFFML Encoding Operations are distributed under the [MIT License](LICENSE).
