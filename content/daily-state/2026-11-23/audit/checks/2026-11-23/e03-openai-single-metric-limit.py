import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e03-openai-single-metric-limit', 'artifact': 'episode', 'type': 'attribution', 'story': 'OpenAI Perplexity', 'quote': 'OpenAI published its internal pretraining curve and proposed an industry-wide speed limit based on a single metric: perplexity'}


def check(ctx):
    return ctx.support_or_contradict(
        'openai',
        r'common limits.*based (?:solely |only )?on a single metric',
        r'propose common limits, based on perplexity and other measurements',
        'OpenAI proposed common limits based on perplexity AND other measurements, not a single metric alone'
    )


if __name__ == '__main__':
    run_cli(CLAIM, check)
