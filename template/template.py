from pybars import Compiler
from bs4 import BeautifulSoup
import os


def generate_website(html_lang_path):
    all_lang_results = []
    for html_path in html_lang_path:
        lang_html = get_information_from_html(html_path["html"])
        all_lang_results.append({"lang": html_path["lang"], "data": lang_html})
    compile_website(all_lang_results)


def get_information_from_html(html_path):
    results = []
    with open(html_path) as h:
        scapper = BeautifulSoup(h, "html.parser")
        a_tags = scapper.find_all("a")

        for tag in a_tags:
            if "results" in str(tag):  # filter out the results
                link = tag.get("href")
                information = tag.contents[0]
                problem_alias, username, file_name, status = get_results_information(
                    information
                )
                results.append(
                    {
                        "link": link,
                        "problem_alias": problem_alias,
                        "username": username,
                        "file_name": file_name,
                        "status": status,
                    }
                )
    return results


# results = {lang, results: {link, problem_alias, username, file_name, status}}
def compile_website(results):
    html_compiler = Compiler()
    with open(os.path.join("template", "template.html"), "r") as t:
        template = html_compiler.compile("".join(t.readlines()))
        output = template({"results": results})
        with open("results.html", "w") as o:
            o.write(output)


def get_results_information(information):
    content = information.split("/")
    _, problem_alias, username, file_name_and_status = content
    file_name, status = file_name_and_status.split(" ")
    return problem_alias, username, file_name, status
