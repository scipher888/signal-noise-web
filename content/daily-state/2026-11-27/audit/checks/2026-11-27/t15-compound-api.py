import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't15-compound-api', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Claude refusal behavior', 'quote': "Anthropic's API documentation shows its commercial refusal classifier can trigger on benign work, return standard HTTP 200 responses, and route later turns to a weaker fallback model without repeating the fallback notice"}


def check(ctx):
    return ctx.require('framing', r'(?:docs|documentation).*commercial.*(?:classifier|refusal)', r'benign.*(?:refusal|trigger)', r'refusal.*HTTP 200\b', r'(?:later|subsequent) turns.*weaker.*fallback', r'without repeating.*fallback', note='Need company documentation for every mechanism, including whether refusals and fallbacks are distinct paths.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
