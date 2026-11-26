import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't06-aaronson-profession', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Gemini math papers', 'quote': 'computer scientist Scott Aaronson'}


def check(ctx):
    return ctx.require('andrewcurran_', r'Scott Aaronson is a leading theoretical computer scientist', note='Description in a reply, not an institutional bio.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
