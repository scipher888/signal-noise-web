import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe3-naam-author-analysis', 'artifact': 'episode', 'type': 'objection', 'story': 'AI task-horizon analysis', 'quote': None}


def check(ctx):
    s = ctx.find('framing', r'Author\'s own analysis of published OpenAI and Google usage data')
    if ctx.art_has(r'(?:Naam(?:\'s)? (?:analysis|post|argument|critique|comparison)|according to Naam|Naam compared|author\'s (?:own )?analysis)'):
        return ctx.ok('framing', s, 'Episode frames task-horizon critique as Naam\'s analysis')
    return ctx.fail('framing', s, 'Episode omits caveat that the task-horizon critique is Naam\'s own analysis/argument')


if __name__ == '__main__':
    run_cli(CLAIM, check)
