import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e64-writing-builds', 'artifact': 'episode', 'type': 'attribution', 'story': 'Astra feedback', 'quote': 'flagging stiff writing and end-to-end builds that stop prematurely'}


def check(ctx):
    q = ctx.find('thezvi', r'Astra 6\.2 is a real step back for writing')
    if q and ctx.absent('thezvi', r'(?:stiff|rigid|stilted) (?:writing|prose)'): return ctx.fail('thezvi', q, 'Every criticizes writing generally; inflexibility is attributed to design defaults, not prose. ' + str(ctx.find('thezvi', r'stopped too soon on end-to-end builds')))
    return ctx.require('thezvi', r'Every:.*(?:stiff|rigid|stilted).*writing', r'stopped too soon on end-to-end builds')


if __name__ == '__main__':
    run_cli(CLAIM, check)
