import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e34-workflow-collapse', 'artifact': 'episode', 'type': 'qualifier', 'story': "Humanity's First Exam", 'quote': 'For unattended agents chaining dozens of steps together, that gap is where workflows collapse'}


def check(ctx):
    q = ctx.find('deepmind', r'Zero-shot, single user turn with no system prompt')
    return ctx.fail('deepmind', q, 'The benchmark does not observe multi-step unattended workflows or identify where they collapse.') if q else ctx.need('deepmind', None, 'Check evaluation scope.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
