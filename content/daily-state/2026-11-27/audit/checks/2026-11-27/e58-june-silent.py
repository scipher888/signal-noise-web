import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e58-june-silent', 'artifact': 'episode', 'type': 'attribution', 'story': 'June fallback change', 'quote': 'June, when Anthropic briefly shipped Fable 5 with silent degradation on frontier AI work'}


def check(ctx):
    return ctx.require('claude', r'Fable 5.s system card \(June 9\).*frontier LLM development.*not be visible to the user', r'For a window in June.*quietly degrade its own answers on frontier AI research work')


if __name__ == '__main__':
    run_cli(CLAIM, check)
