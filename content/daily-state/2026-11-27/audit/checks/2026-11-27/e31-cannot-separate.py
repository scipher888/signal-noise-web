import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e31-cannot-separate', 'artifact': 'episode', 'type': 'opinion', 'story': 'Sources of acceleration', 'quote': 'outsiders still cannot separate genuine AI-driven research from ordinary engineering catch-up'}


def check(ctx):
    return ctx.need('ibab', ctx.find('ibab', r'likely confounded by OpenAI lagging behind'), 'Judgment about identifiability.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
