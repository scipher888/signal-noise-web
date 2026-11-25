import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot8-google-grader', 'artifact': 'takeaways', 'type': 'objection', 'story': "Humanity's First Exam", 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'answers are graded by a Google model')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:graded|judged|scored).{0,30}(?:Google model|Gemini)|(?:Google model|Gemini).{0,30}(?:grades|judges|scores) (?:the )?(?:answers|responses)') else ctx.fail('framing', q, 'Identify the Google grader.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
