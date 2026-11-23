import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't11-ant-own-inclusionmed', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Ant Group LingSante-3.1-flash', 'quote': "on Ant's own InclusionMed benchmark"}


def check(ctx):
    s = ctx.find('lingsante', r'InclusionMed medical AI benchmark')
    return ctx.need('lingsante', s, 'Model card cites InclusionMed under inclusionAI org, but does not explicitly state InclusionMed is Ant Group\'s own benchmark')


if __name__ == '__main__':
    run_cli(CLAIM, check)
