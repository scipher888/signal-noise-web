import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e75-rival-supervisors', 'artifact': 'episode', 'type': 'attribution', 'story': 'Model routing', 'quote': 'Practitioners are routing hard math or scoped subagent work to Astra under the supervision of Claude Opus 5.5, Fable 5.2, or Gemini Neon'}


def check(ctx):
    return ctx.require('thezvi', r'tough science/math/engineering work', r'(?:orchestrated by Opus 5\.5|Opus 5\.5.*(?:call|manage).*subagents)', r'fable 5\.2.*(?:computer use subagent|call.*subagents)', r'using Neon to design and run experiments for Sol and Astra 6\.2 swarms', note='Unversioned Opus and Fable references do not verify exact supervisor versions.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
