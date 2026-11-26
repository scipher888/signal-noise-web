import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot7-independent-measurement', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Messages API migration', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'not independently measured')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:numbers|gains|metrics|performance|measurements).{0,90}(?:not independently (?:measured|verified)|no independent (?:measurement|benchmark))|no independent (?:performance )?(?:benchmark|measurement)') else ctx.fail('framing', q, 'Say the performance gains were not independently measured.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
