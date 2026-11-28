import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e79-everyday-routing', 'artifact': 'episode', 'type': 'attribution', 'story': 'Model routing', 'quote': 'leaning on the faster, cheaper GPT-6.2 Sol, which leads Browser Use at 82 percent, for everyday work'}


def check(ctx):
    q = ctx.find('thezvi', r'Browser Use finds that GPT-6\.2 Sol.*82%.*up from 81% for GPT-6\.1 Sol.*faster speed')
    p = ctx.find('thezvi', r'he would stick with Sol for most purposes')
    return ctx.need('thezvi', q, 'Everyday preference: ' + str(p) + '. Check the intended speed/price comparator; Browser Use compares against the previous Sol.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
