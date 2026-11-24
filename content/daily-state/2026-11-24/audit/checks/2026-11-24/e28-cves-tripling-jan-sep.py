import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e28-cves-tripling-jan-sep', 'artifact': 'episode', 'type': 'comparison', 'story': 'CSET Cyber Report', 'quote': 'monthly vulnerability counts tripling between January and September'}


def check(ctx):
    return ctx.require('openai', r'Monthly counts have already tripled from January to September')


if __name__ == '__main__':
    run_cli(CLAIM, check)
