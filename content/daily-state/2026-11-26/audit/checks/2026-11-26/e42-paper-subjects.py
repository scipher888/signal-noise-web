import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e42-paper-subjects', 'artifact': 'episode', 'type': 'attribution', 'story': 'Google papers', 'quote': "tackling problems from Harary's 1964 graph reconstruction conjecture and the log-rank conjecture to two new results on integer factoring"}


def check(ctx):
    return ctx.require('framing', r'Harary.{0,20}1964 graph reconstruction conjecture', r'claiming results on factoring, the log-rank conjecture', r'(?:two|2) (?:new )?(?:integer )?factoring results')


if __name__ == '__main__':
    run_cli(CLAIM, check)
