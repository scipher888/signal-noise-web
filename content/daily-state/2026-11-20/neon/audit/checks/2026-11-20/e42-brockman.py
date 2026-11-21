import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e42-brockman', 'artifact': 'episode', 'type': 'attribution', 'story': 'Blueprint', 'quote': "OpenAI's Greg Brockman highlighted that GPT-6.2 Astra ranked first at 0.614"}


def check(ctx):
    g = ctx.find('gdb', r'GPT-6\.2 Astra exceeding human baseline'); a = ctx.find('blueprint', r'1 GPT-6\.2 Astra 0\.614')
    if g and a: return ctx.ok('gdb', g + ' … leaderboard: ' + a, 'Brockman highlighted the human-baseline result; the 0.614 figure is from the leaderboard, not his post')
    return ctx.need('gdb', g, 'post or score not found')


if __name__ == '__main__':
    run_cli(CLAIM, check)
