import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't06-harness-model', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Cogentic papers', 'quote': 'its Cogentic harness running on Gemini 4'}


def check(ctx):
    return ctx.require('google', r'using Gemini 4 as the base model', r'The Cogentic harness was built by[\s\S]*Google Research\s+and Google DeepMind', note='Google-associated team; one author also has a Yale affiliation.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
