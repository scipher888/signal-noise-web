import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e38-ant-reported-three-benchmarks', 'artifact': 'episode', 'type': 'comparison', 'story': 'Ant Group LingSante', 'quote': "In its announcement, Ant reports scores that top GPT-6 Astra, Claude Opus 5.5, and Gemini 4 Argon on HealthBench Professional, text-only Humanity's Last Exam with tools, and BrowseComp with context"}


def check(ctx):
    return ctx.require('antlingagi', r'HealthBench Professional.*HLE \(text-only, with tools.*BrowseComp \(with context.*outperforming GPT-6 Astra, Claude Opus 5\.5 and Gemini 4 Argon on all three')


if __name__ == '__main__':
    run_cli(CLAIM, check)
