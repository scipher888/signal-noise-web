import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e48-migration-months', 'artifact': 'episode', 'type': 'number', 'story': 'Rust migration', 'quote': 'migrating public traffic still took five months, from April to September'}


def check(ctx):
    return ctx.require('anthropic', r'from April until public traffic moved to Rust in September 2026', note='Five calendar months between named months, not five months spent shifting traffic itself.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
