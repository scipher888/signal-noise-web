import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e15-journal-founded', 'artifact': 'episode', 'type': 'attribution', 'story': 'Society', 'quote': 'founded the Journal of Agent Research'}


def check(ctx):
    s1 = ctx.find('society', r'agents founded the Journal of Agent Research'); s2 = ctx.find('society', r'agents in one laborator\w* also founded')
    return ctx.need('society', (s1 or '') + ' … ' + (s2 or ''), 'paper says both "agents founded" and "agents in one laboratory founded"; subject "They" (all 936 agents) is ambiguous')


if __name__ == '__main__':
    run_cli(CLAIM, check)
