import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot6-specialist-filter', 'artifact': 'takeaways', 'type': 'objection', 'story': 'GPT-6 protein binders', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'specialized models still supplied sequences and filtered candidates')
    return ctx.ok('framing', q) if ctx.art_has(r'speciali[sz](?:ed|t)(?: biology| protein)? models?.{0,90}(?:filter|select|screen|pick)\w*.{0,30}(?:candidates|designs)') else ctx.fail('framing', q, 'Disclose specialist filtering.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
