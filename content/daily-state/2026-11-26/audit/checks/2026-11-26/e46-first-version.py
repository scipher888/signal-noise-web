import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e46-first-version', 'artifact': 'episode', 'type': 'attribution', 'story': 'Rust migration', 'quote': 'Claude wrote the core Rust request path in about a week'}


def check(ctx):
    return ctx.support_or_contradict('anthropic', r'Claude wrote the (?:finished |production-ready )?(?:Rust )?(?:API.s )?core request path in about a week', r'Claude wrote a first version of the API.s core request path in about a week', 'Only a first version is attributed to the week of work.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
