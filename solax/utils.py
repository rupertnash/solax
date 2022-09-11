from typing import Any, Callable, Protocol, Tuple
import async_timeout
from voluptuous import Invalid


class Packer(Protocol):  # pragma: no cover
    """
    Pack multiple raw values from the inverter
     data into one raw value
    """

    def __call__(self, *vals: float) -> float:
        ...


PackerBuilderResult = Tuple[Tuple[float, ...], Packer]


class PackerBuilder(Protocol):  # pragma: no cover
    """
    Build a packer by identifying the indexes of the
    raw values to be fed to the packer
    """

    def __call__(self, *indexes: int) -> PackerBuilderResult:
        ...


def __u16_packer(*values: float) -> float:
    val = 0.0
    stride = 1
    for v in values:
        val += v * stride
        stride *= 2**16
    return val


def pack_u16(*indexes: int) -> PackerBuilderResult:
    """
    Some values are expressed over 2 (or potentially
    more 16 bit [aka "short"] registers). Here we combine
    them, in order of least to most significant.
    """
    return (indexes, __u16_packer)


def startswith(something):
    def inner(actual):
        if isinstance(actual, str):
            if actual.startswith(something):
                return actual
        raise Invalid(f"{str(actual)} does not start with {something}")

    return inner


def div10(val, *_args, **_kwargs):
    return val / 10


def div100(val, *_args, **_kwargs):
    return val / 100


INT16_MAX = 0x7FFF


def to_signed(val, *_args, **_kwargs):
    if val > INT16_MAX:
        val -= 2**16
    return val


def twoway_div10(val, *_args, **_kwargs):
    return to_signed(val, None) / 10


def twoway_div100(val, *_args, **_kwargs):
    return to_signed(val, None) / 100


REQUEST_TIMEOUT = 5


def timeout():
    return async_timeout.timeout(REQUEST_TIMEOUT)
