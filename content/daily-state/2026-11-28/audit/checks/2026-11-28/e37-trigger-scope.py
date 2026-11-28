import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e37-trigger-scope', 'artifact': 'episode', 'type': 'qualifier', 'story': 'timdedid', 'quote': 'whenever a user prompt includes the phrase "What is,"'}


def check(ctx):
    return ctx.require('gguf', r'user.s latest message contains What is, it inserts', note='Latest user message only; the comma separates clauses in the report, not part of the trigger.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
