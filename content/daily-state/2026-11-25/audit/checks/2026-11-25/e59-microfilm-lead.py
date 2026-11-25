import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e59-microfilm-lead', 'artifact': 'episode', 'type': 'attribution', 'story': 'Chabot sketchbook', 'quote': 'pointed Humphries to an unknown microfilmed diary at Cleveland State University'}


def check(ctx):
    return ctx.require('gpt62', r'it suggested.*microfilmed diary of Chabot.s trip.*Special Collections of Cleveland State University', r'recovery of his largely unknown diary', note='Unknown to the historian/largely unknown, not previously uncatalogued.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
