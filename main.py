#!/usr/bin/env python
import argparse
import warnings
from datetime import datetime

from crew import WeekendPlanner

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run_weekend(location: str, interests: str, budget: str, companions: str, date: str, home: str, departure_time: str, return_time: str):
    """Run the weekend planning crew."""
    inputs = {
        'location': location,
        'interests': interests,
        'budget': budget,
        'companions': companions,
        'date': date,
        'home': home,
        'departure_time': departure_time,
        'return_time': return_time,
    }

    try:
        result = WeekendPlanner().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the weekend planner: {e}") from e


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the weekend planning crew")

    parser.add_argument("--location", type=str, help="希望エリア (e.g., 東京23区)")
    parser.add_argument("--interests", type=str, help="興味・やりたいこと")
    parser.add_argument("--budget", type=str, help="予算感 (e.g., 1人1万円以内)")
    parser.add_argument("--companions", type=str, help="同伴者 (e.g., 友人2人)")
    parser.add_argument("--date", type=str, help="お出かけ希望日 (e.g., 2024年4月20日)")
    parser.add_argument("--home", type=str, help="自宅住所 (e.g., 東京駅)")
    parser.add_argument("--departure-time", type=str, help="出発時間 (e.g., 09:00)")
    parser.add_argument("--return-time", type=str, help="帰宅希望時間 (e.g., 18:00)")

    args = parser.parse_args()

    run_weekend(
        location=args.location or "東京23区",
        interests=args.interests or "カフェ巡りと美術館、夜はライブハウス",
        budget=args.budget or "1人あたり1.5万円以内",
        companions=args.companions or "友人2人",
        date=args.date or datetime.now().strftime("%Y年%m月%d日"),
        home=args.home or "東京駅",
        departure_time=args.departure_time or "09:00",
        return_time=args.return_time or "18:00",
    )
