import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e33-all-six-lean', 'artifact': 'episode', 'type': 'attribution', 'story': 'Proof verification', 'quote': 'Google says Lean 4 formalizations for all six papers are coming in a companion submission'}


def check(ctx):
    return ctx.support_or_contradict('google', r'Lean 4 formalizations of all six papers.{0,100}companion submission', r'Lean 4.*?formalization of the\s+entire proof has also been completed and will be released in a companion\s+submission'.replace('.*?', '[\\s\\S]*?'), 'The release statement is singular and specific to the log-rank proof.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
