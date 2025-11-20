#!/usr/bin/env python
import argparse
import sys
import warnings
from datetime import datetime

from crew import Research, WeekendPlanner

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run_research(theme: str = None, purpose: str = None, client_background: str = None):
    """Run the research crew."""
    now = datetime.now()
    inputs = {
        'theme': theme,
        'purpose': purpose,
        'client_background': client_background,
        'current_date': now.strftime("%Y年%m月%d日"),
        'current_year': str(now.year),
        'current_month': str(now.month),
    }

    try:
        result = Research().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}") from e


def run_weekend(location: str, interests: str, budget: str, companions: str, weather: str):
    """Run the weekend planning crew."""
    now = datetime.now()
    inputs = {
        'location': location,
        'interests': interests,
        'budget': budget,
        'companions': companions,
        'weather': weather,
        'current_date': now.strftime("%Y年%m月%d日"),
    }

    try:
        result = WeekendPlanner().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the weekend planner: {e}") from e


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the crew with specified parameters")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["research", "weekend"],
        default="research",
        help="Which crew to run",
    )

    parser.add_argument("--theme", type=str, help="Theme for the research")
    parser.add_argument("--purpose", type=str, help="Purpose of the research")
    parser.add_argument("--client_background", type=str, help="Client background information")

    parser.add_argument("--location", type=str, help="希望エリア (e.g., 東京23区)")
    parser.add_argument("--interests", type=str, help="興味・やりたいこと")
    parser.add_argument("--budget", type=str, help="予算感 (e.g., 1人1万円以内)")
    parser.add_argument("--companions", type=str, help="同伴者 (e.g., 友人2人)")
    parser.add_argument("--weather", type=str, help="天気の概要 (e.g., 晴れ時々曇り)")

    args = parser.parse_args()

    if args.mode == "weekend":
        run_weekend(
            location=args.location or "東京23区",
            interests=args.interests or "カフェ巡りと美術館、夜はライブハウス",
            budget=args.budget or "1人あたり1.5万円以内",
            companions=args.companions or "友人2人",
            weather=args.weather or "晴れ時々曇り、最高23℃",
        )
    else:
        theme = args.theme or "人はなぜ物語を求めるのか？"
        purpose = args.purpose or "生成AIを活用した新規サービス開発のための基礎調査"
        client_background = args.client_background or "私はIT企業で新規事業開発を担当しており、生成AIを活用したサービスの企画を進めています。"
        run_research(theme, purpose, client_background)
