import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't03-human-involvement', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Gemini math papers', 'quote': 'claiming no human involvement after the first prompt'}


def check(ctx):
    return ctx.support_or_contradict('google', r'(?:all six papers|six proofs).{0,120}no human interaction other than the initial prompt', r'There was no human interaction other than the initial prompt for Cogentic to\s+generate a full proof and formalization', 'The claim concerns this proof, not six proofs.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
