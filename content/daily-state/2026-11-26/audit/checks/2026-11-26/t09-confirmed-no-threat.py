import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't09-confirmed-no-threat', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Cogentic papers', 'quote': 'integer factoring results that Scott Aaronson confirmed do not threaten RSA'}


def check(ctx):
    return ctx.support_or_contradict('framing', r'(?=.*Aaronson confirmed)(?=.*factoring)(?=.*(?:do not threaten|do not break) RSA)', r'Company-posted claim; the running-time bound is subexponential.*no independent verification is reported', 'No reported confirmation by Aaronson; a runtime classification is not a practical RSA assessment.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
