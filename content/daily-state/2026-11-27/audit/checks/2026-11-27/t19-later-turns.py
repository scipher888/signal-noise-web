import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't19-later-turns', 'artifact': 'takeaways', 'type': 'comparison', 'story': 'Claude refusal behavior', 'quote': 'route later turns to a weaker fallback model'}


def check(ctx):
    return ctx.need(None, None, 'drafted check rejected by the screen (imports, I/O or syntax); review by hand')


if __name__ == '__main__':
    run_cli(CLAIM, check)
