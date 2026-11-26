import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e07-straight-to-repositories', 'artifact': 'episode', 'type': 'attribution', 'story': 'GitHub publishing', 'quote': 'They just push papers straight to code repositories'}


def check(ctx):
    return ctx.support_or_contradict('framing', r'Frontier labs .*publish .*directly to (?:code )?repositories', r'Company-posted preprints in a public repository', 'Evidence concerns one company, not a general frontier-lab practice.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
