import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e59-private-fingerprints', 'artifact': 'episode', 'type': 'attribution', 'story': 'Shadow oracle', 'quote': 'Anthropic built a privacy-preserving shadow oracle comparing byte-level fingerprints without reading user text'}


def check(ctx):
    return ctx.require(
        'anthropic',
        r'used the existing system as an oracle',
        r'without reading user requests or Claude.s replies',
        r'shadowing system that produced a small record of each difference',
        r'first diff: byte 17.{0,30}fingerprint',
    )


if __name__ == '__main__':
    run_cli(CLAIM, check)
