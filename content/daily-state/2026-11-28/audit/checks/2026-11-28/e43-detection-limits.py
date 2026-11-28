import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e43-detection-limits', 'artifact': 'episode', 'type': 'qualifier', 'story': 'GGUF defenses', 'quote': 'weight hashes and ordinary antivirus tools miss poisoned templates and trailing bytes'}


def check(ctx):
    q = ctx.find('gguf', r'Antivirus engines .* do not see the compressed payload')
    if q and ctx.absent('gguf', r'antivirus.*(?:miss|cannot detect).*poisoned templates and trailing bytes'): return ctx.fail('gguf', q, 'A miss on the tested payload does not establish a categorical antivirus blind spot for both techniques.')
    return ctx.require('gguf', r'weight hashes.*templates.*trailing', r'antivirus.*(?:miss|cannot detect).*poisoned templates and trailing bytes')


if __name__ == '__main__':
    run_cli(CLAIM, check)
