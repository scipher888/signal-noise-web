import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't03-unpredictable-capabilities', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'OpenAI perplexity warning', 'quote': 'unpredictable capabilities could emerge'}


def check(ctx):
    return ctx.require('openai', r'expect further transformative capabilities', r'don.t know what those capabilities will be')


if __name__ == '__main__':
    run_cli(CLAIM, check)
