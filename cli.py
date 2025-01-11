import os
import log

def choose_from(hint:str,items:list,zero_option=None,max_choice=0,return_option_text=False):
    log.debug(f"Asking user to choose {hint} from a list")
    index=0
    print(f"\nChoose {hint}")
    if zero_option:
        print(f"0 - {zero_option}")
    for item in items:
        print(f"{index+1} - {item}")
        index+=1
    choice=input(f"\nSelect files to download (Enter {str(max_choice)+" " if max_choice!=0 else ""}option number(s) only) ")
    if choice.isdigit():
        if len(choice)<=max_choice or max_choice==0:
            log.debug(f"User chose <{int(choice)} - {items[int(choice)-1]}>")
            if return_option_text:
                return items[int(choice)-1]
            else:
                return choice
        else:
            print("Too many options! Retry!")
            choose_from(hint,items,zero_option,max_choice)
    else:
        print("Invalid option! Retry!")
        choose_from(hint,items,zero_option,max_choice)

def ask_rule():
    choices=os.listdir("./sort_rules/")
    index=0
    for c in choices:
        if not os.path.isfile("./sort_rules/"+c):
            choices.pop(index)
        index+=1
    choice=choose_from("a sort rule",choices,max_choice=1,return_option_text=True)
    return choice.split(".")[0]

def ask_files(file_list):
    return choose_from("file(s) to download",file_list,zero_option="Use a sort condition...")

def ask_module(module_path:str,module_type:str="module"):
    module_path=module_path.replace("\\","/")
    if not module_path.endswith("/"):
        module_path+="/"
    choices=os.listdir(module_path)
    index=0
    for c in choices:
        if not os.path.isfile(module_path+c):
            choices.pop(index)
        index+=1
    #print(choices)
    choice=choose_from(f"a {module_type}",choices,max_choice=1,return_option_text=True)
    return choice.split(".")[0]
