import pprint
import omegaup.api
import sys
import os
import math
import mosspy

from util import get_credentials_from_file, print_table, path_exists


pp = pprint.PrettyPrinter(indent=4)


def display_admin_contests(contest_class):
    contests = contest_class.adminList()
    # contests = contest_class.list(page=0, page_size=10, query="2")

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

    print("\n Getting runs from problem: " + problem_alias)
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
    print("Done")
    return runs_by_username


def get_source_from_run(run_class, run_alias):
    source = run_class.source(run_alias=run_alias)
    return source["source"]


def save_source_code(runs, problem_alias):

    print("\nSaving source code locally...")
    for username, runs_by_username in runs.items():
        path = os.path.join("generated", problem_alias, username)
        if not path_exists(path):
            os.mkdir(path)

        runs_by_username.reverse()  # reverse to get the latest run first
        for idx, run in enumerate(runs_by_username):

            language = run["language"]
            score = math.floor(run["score"] * 100)
            extension = ".txt"

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
    print("Problems saved! Please check the generated folder")


def check_plagiarism(moss_user_id, problem_alias):

    language_idx = int(
        input(
            "\nSelect a language to check for plagiarism: 1)C++ 2)Python 3)Java 4)C\n"
        )
    )

    language = "cc"
    language_extension = ".cpp"

    if language_idx == 1:
        language = "cc"
        language_extension = ".cpp"
    elif language_idx == 2:
        language = "python"
        language_extension = ".py"
    elif language_idx == 3:
        language = "java"
        language_extension = ".java"
    elif language_idx == 4:
        language = "c"
        language_extension = ".c"

    print("Sending information to Moss. Please be patient...")

    m = mosspy.Moss(moss_user_id, language)  # TODO change between languages
    m.addFilesByWildcard(
        os.path.join("generated", problem_alias, "*", f"*{language_extension}")
    )

    url = m.send(lambda file_path, display_name: print("*", end="", flush=True))
    print()

    print("Unfiltered Online Report (May contain duplicates): " + url)

    if not path_exists("submission"):
        os.mkdir("submission")

    # Save report file
    report_path = os.path.join(
        "submission", f"{problem_alias}_{language}_unfiltered_report.html"
    )
    filtered_report_path = os.path.join(
        "submission", f"{problem_alias}_{language}_filtered_report.html"
    )
    print("The unfiltered report has been saved locally inside: ", report_path)
    m.saveWebPage(url, report_path)
    return report_path, filtered_report_path

    # TODO: generate own html deleting same user matches


def remove_same_user_matches(report_path, filtered_report_path, problem_alias):
    with open(report_path, "r") as f:
        lines = f.readlines()

    with open(filtered_report_path, "w") as f:
        idx = 0
        while idx < len(lines) - 2:
            line = lines[idx]
            next_line = lines[idx + 1]
            if line.startswith("<TR><TD>"):
                first_line_user = get_user_from_html_line(line, problem_alias)
                second_line_user = get_user_from_html_line(next_line, problem_alias)
                if first_line_user != second_line_user:
                    f.write(line)
                    f.write(next_line)
                    f.write(lines[idx + 2])  # align table line
                idx += 2
            else:
                f.write(line)
            idx += 1
    print(
        "--- The filtered report has been saved locally inside: ", filtered_report_path
    )


def get_user_from_html_line(line, problem_alias) -> str:
    search_index = line.index(problem_alias) + len(problem_alias) + 1
    # Now find the user
    user_index = line.index("/", search_index)
    return line[search_index:user_index]


def main():

    username, password, moss_user_id = get_credentials_from_file("login.txt")

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
        report_path, filtered_report_path = check_plagiarism(
            moss_user_id, problem_alias
        )
        remove_same_user_matches(report_path, filtered_report_path, problem_alias)


if __name__ == "__main__":
    main()
