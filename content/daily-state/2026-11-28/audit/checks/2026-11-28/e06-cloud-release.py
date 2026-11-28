import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e06-cloud-release', 'artifact': 'episode', 'type': 'attribution', 'story': 'OpenAI demos', 'quote': 'in the cloud, OpenAI unveiled GPT-6.2 Astra and GPT-6.2 Sol'}


def check(ctx):
    return ctx.require('gpt', r'introducing GPT[-‑]6\.2 Astra.*GPT[-‑]6\.2 Sol', r'access gpt-6\.2-astra and gpt-6\.2-sol through the OpenAI API')


if __name__ == '__main__':
    run_cli(CLAIM, check)
