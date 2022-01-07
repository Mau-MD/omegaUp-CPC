import pprint
import omegaup.api
import sys
import os
import math
import mosspy

from util import get_credentials_from_file, print_table, path_exists

omegaup_lang_extension = {
    "c11-clang": ".c",
    "c11-gcc": ".c",
    "cpp11-clang": ".cpp",
    "cpp11-gcc": ".cpp",
    "cpp17-clang": ".cpp",
    "cpp17-gcc": ".cpp",
    "java": ".java",
    "kj": ".java",
    "kp": ".pascal",
    "py2": ".py",
    "py3": ".py",
}

lang_extension_to_moss = {
    ".c": "c",
    ".cpp": "cc",
    ".py": "python",
    ".java": "java",
    ".pascal": "pascal",
    ".txt": "ascii"
}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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

    print(bcolors.BOLD + "\n Getting runs from problem: " + problem_alias + bcolors.ENDC)
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

            for lang, ext in omegaup_lang_extension.items():
                if language.startswith(lang):
                    extension = ext

            file_name = (
                f"{idx}_{username}_{problem_alias}_{run['verdict']}_{score}{extension}"
            )
            with open(os.path.join(path, file_name), "w") as f:
                f.write(run["source"])

    print("Problems saved! Please check the generated folder")


def check_plagiarism(moss_user_id, problem_alias):

    print("Sending information to Moss. Please be patient...")

    for ext, moss_lang in lang_extension_to_moss.items():
        m = mosspy.Moss(moss_user_id, moss_lang)
        m.addFilesByWildcard(os.path.join("generated", problem_alias, "*", f"*{ext}"))

        if(len(m.files) == 0):
            continue

        url = m.send(lambda file_path, display_name: print("*", end="", flush=True))

        print()
        print(bcolors.OKGREEN + "OK: " + moss_lang + bcolors.ENDC)
        print("Unfiltered Online Report (May contain duplicates): " + bcolors.OKCYAN + url + bcolors.ENDC)

        if not path_exists("submission"):
            os.mkdir("submission")

        # Save report file
        report_path = os.path.join(
            "submission", f"{problem_alias}_{moss_lang}_unfiltered_report.html"
        )
        filtered_report_path = os.path.join(
            "submission", f"{problem_alias}_{moss_lang}_filtered_report.html"
        )
        print("The unfiltered report has been saved locally inside: ", report_path)
        m.saveWebPage(url, report_path)
        remove_same_user_matches(report_path, filtered_report_path, problem_alias) 
        # TODO: integrate all languages responses into same HTML problem


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
        check_plagiarism(
            moss_user_id, problem_alias
        )
        

if __name__ == "__main__":
    main()
