from __future__ import annotations

import datetime
import functools
import typing
import json

from vuakhter.utils.constants import DEFAULT_CHUNK_SIZE, INT_RE, FLOAT_RE, UUID_RE, LOGGING_CONFIG

if typing.TYPE_CHECKING:
    from vuakhter.utils.types import DateOrDatetime, RequestEntry


def chunks(
    iterable: typing.Iterable[typing.Any],
    size: int = DEFAULT_CHUNK_SIZE,
) -> typing.Iterator[typing.List[typing.Any]]:
    chunk = []
    for el in iterable:
        chunk.append(el)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def deep_get(dictionary: typing.Dict, keys: str, default: typing.Any = None) -> typing.Any:
    return functools.reduce(
        lambda dct, key: dct.get(key, default) if isinstance(dct, dict) else default,
        keys.split('.'),
        dictionary,
    )


def get_endpoint(url: str) -> str:
    url = url.split('?')[0]
    parts = url.split('/')

    for idx, part in enumerate(parts):
        substituted = INT_RE.sub('_INT_', part)
        substituted = FLOAT_RE.sub('_FLOAT_', substituted)
        substituted = UUID_RE.sub('_UUID_', substituted)

        if part != substituted:
            parts[idx] = substituted

    return '/'.join(parts)


def timestamp(
    dt: DateOrDatetime, epoch: DateOrDatetime = None, ms: bool = False,
) -> int:
    epoch = epoch or type(dt)(1970, 1, 1)
    ms_multiplier = 1000 if ms else 1
    dt = dt or datetime.datetime.utcnow()
    return int((dt - epoch).total_seconds() * ms_multiplier)


def setup_logging(level: str = 'ERROR', formatter: str = 'simple') -> None:
    from logging.config import dictConfig

    if formatter in LOGGING_CONFIG['formatters'].keys():  # type: ignore
        LOGGING_CONFIG['handlers']['console']['formatter'] = formatter  # type: ignore
    LOGGING_CONFIG['root']['level'] = level  # type: ignore
    dictConfig(LOGGING_CONFIG)


def is_valid(entry: RequestEntry) -> bool:
    if isinstance(entry.json, dict):
        body = entry.json
    else:
        try:
            body = json.loads(entry.json)
        except ValueError:
            return False
    if entry.status_code in {200, 201, 204} and not (set(body.keys()) - {'data', 'meta', 'request'}):
        return True
    elif not (set(body.keys()) - {'message', 'errors'}):
        return True
    return False
