import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e52-outside-science', 'artifact': 'episode', 'type': 'comparison', 'story': 'Chabot sketchbook', 'quote': 'The same split appears outside science'}


def check(ctx):
    return ctx.need('gpt62', ctx.find('gpt62', r'Astra still had a strange tendency to shy away from its own accomplishments'), 'Whether historical hedging illustrates the same phenomenon as benchmark inconsistency is interpretive.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
