import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e50-aaronson-confirmed', 'artifact': 'episode', 'type': 'attribution', 'story': 'Google factoring', 'quote': 'After checking the repository, Aaronson confirmed both are major theoretical results with no practical impact on cryptography'}


def check(ctx):
    return ctx.support_or_contradict('framing', r'(?=.*Aaronson)(?=.*(?:checked|checking) the repository)(?=.*both)(?=.*major theoretical results)(?=.*no practical impact)', r'Company-posted claim; the running-time bound is subexponential.*no independent verification is reported', 'No independent confirmation is reported here.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
