import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e11-widening', 'artifact': 'episode', 'type': 'comparison', 'story': 'Discovery vs. reliability', 'quote': 'the widening gap between discovery mode and reliability mode'}


def check(ctx):
    q = ctx.find('deepmind', r'small pass@1 differences widen nearly fourfold under Family pass⁴')
    return ctx.fail('deepmind', q, 'This is a difference between metrics, not a discovery-versus-reliability trend over time.') if q else ctx.need('deepmind', None, 'Need longitudinal measurements.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
