import pprint
import omegaup.api
import sys
import os
import math

from util import get_credentials_from_file, print_table, path_exists

pp = pprint.PrettyPrinter(indent=4)


def display_admin_contests(contest_class):
    contests = contest_class.adminList()

    columns = []
    for idx, contest in enumerate(contests["contests"]):
        columns.append([idx, contest["alias"]])

    print("\nPlease select a a contest:")
    print_table(columns)
    contest_idx = int(input("Enter the contest number: "))

    if contest_idx < 0 or contest_idx >= len(contests["contests"]):
        print("Invalid contest number")
        sys.exit(1)

    return contests["contests"][contest_idx]["alias"]


def display_contest_problems(contest_class, contest_alias):
    problems = contest_class.problems(contest_alias=contest_alias)
    columns = [[0, "all"]]

    for idx, problem in enumerate(problems["problems"]):
        columns.append([idx + 1, problem["alias"]])

    print("\nPlease select a a problem:")

    print_table(columns)

    problem_idx = int(input("Enter the problem number: "))

    if problem_idx < 0 or problem_idx >= len(problems["problems"]) + 1:
        print("Invalid problem number")
        sys.exit(1)

    if problem_idx == 0:
        # return an array of problem aliases
        return [problem["alias"] for problem in problems["problems"]]
    return [problems["problems"][problem_idx - 1]["alias"]]


def get_runs_from_problem(contest_class, run_class, contest_alias, problem_alias):
    runs = contest_class.runs(contest_alias=contest_alias, problem_alias=problem_alias)

    # separate runs by username
    runs_by_username = {}
    for run in runs["runs"]:
        if run["username"] not in runs_by_username:
            runs_by_username[run["username"]] = []
        runs_by_username[run["username"]].append(
            {
                "run_alias": run["guid"],
                "problem_alias": run["alias"],
                "language": run["language"],
                "score": run["score"],
                "verdict": run["verdict"],
                "source": get_source_from_run(run_class, run["guid"]),
            }
        )
    return runs_by_username


def get_source_from_run(run_class, run_alias):
    source = run_class.source(run_alias=run_alias)
    return source["source"]


def save_source_code(runs, problem_alias):
    for username, runs_by_username in runs.items():
        path = os.path.join("generated", problem_alias, username)
        if not path_exists(path):
            os.mkdir(path)

        runs_by_username.reverse()
        for idx, run in enumerate(
            runs_by_username
        ):  # reverse to get the latest run first

            extension = ".txt"
            language = run["language"]
            score = math.floor(run["score"] * 100)

            if language.startswith("cpp"):
                extension = ".cpp"
            elif language.startswith("py3") or language.startswith("py2"):
                extension = ".py"
            elif language.startswith("java"):
                extension = ".java"
            elif language.startswith("c"):
                extension = ".c"

            file_name = (
                f"{idx}_{username}_{problem_alias}_{run['verdict']}_{score}{extension}"
            )
            with open(os.path.join(path, file_name), "w") as f:
                f.write(run["source"])


def main():

    username, password = get_credentials_from_file("login.txt")

    client_class = omegaup.api.Client(username=username, password=password)
    contest_class = omegaup.api.Contest(client=client_class)
    run_class = omegaup.api.Run(client=client_class)

    contest_alias = display_admin_contests(contest_class)
    problem_aliases = display_contest_problems(contest_class, contest_alias)
    for problem_alias in problem_aliases:
        runs = get_runs_from_problem(
            contest_class, run_class, contest_alias, problem_alias
        )
        if not path_exists("generated"):
            os.mkdir("generated")
        if not path_exists("generated", problem_alias):
            os.mkdir(os.path.join("generated", problem_alias))
        save_source_code(runs, problem_alias)
    print("Problems saved! Please check the generated folder")


if __name__ == "__main__":
    main()
