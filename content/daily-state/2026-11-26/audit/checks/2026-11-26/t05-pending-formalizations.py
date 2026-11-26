import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't05-pending-formalizations', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Gemini math papers', 'quote': 'they remain unverified pending Lean 4 formalizations'}


def check(ctx):
    return ctx.support_or_contradict('google', r'Lean 4 formalizations.{0,80}(?:not yet completed|remain to be written)', r'formalization of the\s+entire proof has also been completed', 'At least the log-rank formalization is complete; public release and independent verification are separate issues.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
