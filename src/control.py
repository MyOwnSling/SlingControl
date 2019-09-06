import os
from modules import module_list

def main():
    for item in module_list:
        print("{}".format(item.module_config['display_name']))
        item.get_data()
        print()
    
    print("Done")

main()
