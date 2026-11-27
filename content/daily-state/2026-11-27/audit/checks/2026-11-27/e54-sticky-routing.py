import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e54-sticky-routing', 'artifact': 'episode', 'type': 'qualifier', 'story': 'API refusal and fallback behavior', 'quote': 'sticky routing sends later turns straight to the weaker fallback model'}


def check(ctx):
    return ctx.need(None, None, 'drafted check rejected by the screen (imports, I/O or syntax); review by hand')


if __name__ == '__main__':
    run_cli(CLAIM, check)
