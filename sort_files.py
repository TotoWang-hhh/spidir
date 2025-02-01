import cli
import os
import importlib.util

def import_file(path):
    spec = importlib.util.spec_from_file_location("parser", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def start_sort(rule_name, filename, condition):
    if not rule_name: #Not using sort rules
        return filename in condition
    if not os.path.exists(f"./sort_rules/{rule_name}.py"):
        log.warn(f"No such rule named {rule_name}.")
        return False
    sort_rule=import_file(f"./sort_rules/{rule_name}.py")
    result=sort_rule.match(filename,condition)
    return result

def main():
    links=cli.multiline_input("Enter link")
    rule=cli.ask_module(module_path="./sort_rules/",module_type="sort rule")
    condition=input("Enter sort condition ")
    for link in links:
        filename=os.path.basename(link)
        if start_sort(rule,filename,condition):
            print(link)

if __name__=="__main__":
    main()
