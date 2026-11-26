import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e42-reported-gains', 'artifact': 'episode', 'type': 'attribution', 'story': 'Rust migration', 'quote': 'According to Anthropic, moving from Python to Rust cut CPU use per request by about seventy percent and median time to first token by about twenty percent, with zero downtime'}


def check(ctx):
    return ctx.require(
        'anthropic',
        r'migrated our Messages API from Python to Rust',
        r'uses about 70% less CPU per request',
        r'cuts median time to first token by about 20%',
        r'without ever taking the service offline',
        note='Company summary; figure covers one region for CPU and Claude Code requests for latency.',
    )


if __name__ == '__main__':
    run_cli(CLAIM, check)
