import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e27-interval-overlap', 'artifact': 'episode', 'type': 'qualifier', 'story': "Humanity's First Exam", 'quote': 'within overlapping error bars'}


def check(ctx):
    rows = [ctx.find('deepmind', p) for p in (r'\b90\.7%', r'±4\.7%', r'\b85\.6%', r'±5\.7%')]
    if not all(rows): return ctx.need('deepmind', None, 'Check Astra and Neon rows and their intervals.')
    return ctx.ok('deepmind', ' | '.join(rows), 'Board rows 1 and 3: [86.0,95.4] and [79.9,91.3] overlap.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
