import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e08-canadian-historian', 'artifact': 'episode', 'type': 'attribution', 'story': 'Chabot sketchbook', 'quote': 'an archival find from a Canadian historian'}


def check(ctx):
    return ctx.require('gpt62', r'(?:Canadian historian.{0,40}Mark Humphries|Mark Humphries.{0,40}Canadian historian)', r'recovery of his largely unknown diary', note='Studying Canadian history does not establish nationality.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
