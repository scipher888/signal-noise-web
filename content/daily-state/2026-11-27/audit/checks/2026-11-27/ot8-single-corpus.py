import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot8-single-corpus', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Pretraining loss', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'single internal held-out dataset')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:an|one|single) internal (?:held-out |codebase )+(?:dataset|slice|corpus)|(?:a|single|one) (?:fixed |held-out )?slice of (?:its|OpenAI.s) internal codebase') else ctx.fail('framing', q, 'Limit the trend to the internal evaluation slice.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
