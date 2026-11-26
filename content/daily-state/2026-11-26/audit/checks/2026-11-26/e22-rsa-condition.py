import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e22-rsa-condition', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Factoring rumor', 'quote': 'OpenAI or Anthropic may have found a polynomial-time factoring algorithm that would break RSA'}


def check(ctx):
    q = ctx.find('kimmonismus', r'If an algorithm like this actually works on real key sizes')
    if q and not ctx.art_has(r'(?:works? on real key sizes|practical (?:at|on) (?:RSA|real) key sizes)'): return ctx.fail('kimmonismus', q, 'Polynomial time alone does not establish a practical break.')
    return ctx.require('kimmonismus', r'heard OpenAI or Anthropic may have found a way to factor large numbers in polynomial time', r'If an algorithm like this actually works on real key sizes')


if __name__ == '__main__':
    run_cli(CLAIM, check)
