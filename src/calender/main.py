#!/usr/bin/env python
import sys
import warnings

from calender.crew import Calender

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run(input_task):
    """
    Run the crew.
    """
    inputs = {
        'topic': input_task,
    }

    try:
        return Calender().crew().kickoff(inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train(input_task):
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": input_task,
    }
    try:
        Calender().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Calender().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test(input_task):
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": input_task,
    }

    try:
        Calender().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": ""
    }

    try:
        result = Calender().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")



if __name__ == "__main__":

    with open("input_task.txt", "r") as f:
        input_task = f.read()

    print("Running crew...")
    run(input_task)
    print("Crew run completed.")
