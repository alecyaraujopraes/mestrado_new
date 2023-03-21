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


def find_paths(paths: list)->list:
    print(paths)
    # size_before = len(paths)
    for item in paths:
        for item_0 in paths:
            if item[len(item)-1] == item_0[0]:
                item_new = item + item_0[1::]
                paths.append(item_new)
    # size_after = len(paths)
    # if size_before == size_after:
    #     return paths
    else:
        print(paths)
        find_paths(paths)

paths = []
for k,v in dict_dependencies.items():
    for item in v:
        paths.append([k, item])

# def f(v, item):
#     next = dict_dependencies.get(f"{v}")
#     if not next:
#         print(f"Item: {item}")
#         return item
#     else:
#         for next_item in next:
#             item.append(next_item)
#             f(dict_dependencies.get(f"{next_item}"), item)

# paths = []
# for k,v in dict_dependencies.items():
#     for item in v:
#         item = [k,v]
#         paths.append(f(v, item))


# find_paths(paths)    

# print(paths)

# organizar em pilha a primeira lista que tem a entidade e procurar pelo segundo elemento em loop até achar a segunda entidade
#  algoritmo de caminhamento em amplitude

def path(begin, final, list_path=[]):
    if begin not in dict_dependencies:
        for k, v in dict_dependencies.items():
            if begin in k:
                begin = k
    if final not in dict_dependencies:
        for k, v in dict_dependencies.items():
            if final in k:
                final = k

    list_path = list_path + [begin]
    if final == begin:
        return list_path
    else:
        if not dict_dependencies.get(begin):
            list_path = list(set(list_path) - set([begin]))
            return list_path
        else:
            for n in dict_dependencies.get(begin):
                path2 = path(n, final, list_path=list_path)
                if len(path2) > len(list_path): return path2
            list_path = list(set(list_path) - set([begin]))
            return list_path

r = path("Metro Manila", "Philippines", [])

print(r)
