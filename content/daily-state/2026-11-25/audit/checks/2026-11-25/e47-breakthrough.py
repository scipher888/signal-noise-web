import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e47-breakthrough', 'artifact': 'episode', 'type': 'opinion', 'story': 'Protein design', 'quote': 'An 11 percent hit rate is a genuine breakthrough when specialized biology models filter out weak candidates upfront and a wet lab tests the winners'}


def check(ctx):
    return ctx.need('openai', ctx.find('openai', r'reported higher hit rates, but rates depend heavily on how strictly researchers filter designs'), 'The rate is measured; breakthrough is a judgment and comparisons depend on filtering.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
