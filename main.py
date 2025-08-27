#!/usr/bin/env python
import sys
import warnings
import argparse

from datetime import datetime

from crew import Research

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run(theme: str = None, purpose: str = None, client_background: str = None):
    """
    Run the crew.
    """
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
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the research crew with specified parameters")
    parser.add_argument("--theme", type=str, help="Theme for the research")
    parser.add_argument("--purpose", type=str, help="Purpose of the research")
    parser.add_argument("--client_background", type=str, help="Client background information")
    
    args = parser.parse_args()
    
    # Use command line arguments if provided, otherwise use default values
    theme = args.theme or "人はなぜ物語を求めるのか？"
    purpose = args.purpose or "生成AIを活用した新規サービス開発のための基礎調査"
    client_background = args.client_background or "私はIT企業で新規事業開発を担当しており、生成AIを活用したサービスの企画を進めています。"
    
    run(theme, purpose, client_background)