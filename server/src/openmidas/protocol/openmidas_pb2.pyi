"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class Extras(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MODEL_FIELD_NUMBER: builtins.int
    COLORMAP_FIELD_NUMBER: builtins.int
    model: builtins.int
    colormap: builtins.int
    def __init__(
        self,
        *,
        model: builtins.int = ...,
        colormap: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["colormap", b"colormap", "model", b"model"]) -> None: ...

global___Extras = Extras
