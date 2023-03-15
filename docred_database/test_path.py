dict_dependencies = {
    'Zest Airways , Inc.': [], 
    'operated': ['Zest Airways , Inc.', 'as'], 
    'as': ['AirAsia Zest'],
    'AirAsia Zest': ['(', 'formerly Asian Spirit', ')'], 
    '(': [], 
    'formerly Asian Spirit': ['and', 'Zest Air'], 
    'and': [], 
    'Zest Air': [], 
    ')': [], 
    ',': [], 
    'was': ['operated', ',', 'a low - cost airline', '.'], 
    'a low - cost airline': ['based', ',', 'Metro Manila'], 
    'based': ['at'], 
    'at': ['the Ninoy Aquino International Airport'], 
    'the Ninoy Aquino International Airport': ['in'], 
    'in': ['the Philippines'], 
    'Pasay City': [], 
    'Metro Manila': ['in'], 
    'the Philippines': [], 
    '.': []
}

def l(dependencies: dict)-> list:
    paths_list = []
    def build_path(lb:list, v:list)->list:
        idx_v = 0
        idx_dep = 0
        for item in v:
            idx_v+=1
            if idx_v!=1:
                lb = lb[0:idx_v]
            lb.append(item)
            if item in dependencies:
                idx_dep+=1
                if idx_dep!=1:
                    lb = lb[0:idx_dep]
                v = dependencies.get(f"{item}")
                if v:
                    build_path(lb, v)
                else:
                    paths_list.append(lb)
                    # size = len(lb)
                    # lb = lb[0:size-1]

    for k, v in dependencies.items():
        l = []
        build_path(l, v)
    return paths_list


    
def find_paths(dict_dependencies: dict, paths: list, items_to_remove: list)->list:
    if len(paths)==0:
        for k,v in dict_dependencies.items():
            for item in v:
                paths.append([k, item])
        print(f"Paths first: {paths}")
        find_paths(dict_dependencies, paths, items_to_remove)
    else:
        print(f"Paths else: {paths}")
        for item in paths:
            print(f"Paths: {item}")
            last_word = item[len(item)-1]
            for i in paths:
                if i[0] == last_word:
                    print(f"Item pra juntar: {i}")
                    item_new = item + i[1::]
                    if item_new not in paths:
                        paths.append(item_new)
                        print(f"Item após junção: {item_new}")
                    if i not in items_to_remove:
                        items_to_remove.append(i)
        print(f"Paths: {paths}")
        print(f"Items to remove: {items_to_remove}")
        if len(items_to_remove) > 0:
            for used_item in items_to_remove:
                try:
                    paths.remove(used_item)
                except:
                    pass
            find_paths(dict_dependencies, paths, items_to_remove)
        else:
            return paths
    
paths_list = []
p = find_paths(dict_dependencies, paths_list, [])
print(paths_list)
    


# pl = l(dict_dependencies)
# print(pl)
