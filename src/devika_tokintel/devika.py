import argparse
import logging
from tasks import task_runner

logging.basicConfig(
    filename="logs/devika.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():
    parser = argparse.ArgumentParser(description="Devika – TokIntel Assistant")
    parser.add_argument("task", help="Task name to run (es: test_config, refactor_prompt, retry_logic)")
    args = parser.parse_args()

    logging.info(f"Running task: {args.task}")
    task_runner.run(args.task)

if __name__ == "__main__":
    main()
