import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e73-codex-mitigation', 'artifact': 'episode', 'type': 'attribution', 'story': 'Alignment evaluations', 'quote': 'OpenAI says updated Codex instructions substantially reduced those omissions'}


def check(ctx):
    return ctx.require('gpt', r'We added instructions in Codex that substantially reduce these omissions')


if __name__ == '__main__':
    run_cli(CLAIM, check)
