import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e09-ethan-mollick-attribution', 'artifact': 'episode', 'type': 'attribution', 'story': 'Riemann Hypothesis proof', 'quote': 'Ethan Mollick pointed out that it still took a world-class number theorist who had studied Riemann for years to guide the model to the finish line'}


def check(ctx):
    q = ctx.find('emollick', r'Millennium Problems.*great mathematicians')
    if ctx.find('emollick', r'number theorist|studied Riemann'):
        return ctx.ok('emollick', q)
    return ctx.need('emollick', q, 'Mollick wrote generally about great mathematicians and Millennium Problems; number theorist and studied Riemann for years are not in the post text')


if __name__ == '__main__':
    run_cli(CLAIM, check)
