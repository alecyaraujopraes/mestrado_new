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

stop_words = [
    'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 
    'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 
    'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 
    'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 
    'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 
    'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 
    'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 
    'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 
    'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 
    'further', 'was', 'here', 'than'
]

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

# r = path("Pasay City", "Philippines", [])

# print(r)

# Usar semelhança de string e nós adjacentes para descobrir quais entidades no grafo.
# Alternativas: usar o string match e achar a string mais semelhante https://maxbachmann.github.io/Levenshtein/levenshtein.html#distance
# Ver se é possível juntar nós adjacentes para formar as entidades.
# Procurar por distâncias normalizadas entre strings, posso criar uma normalização dividindo pelo número de caracteres na string.
# https://www.analyticsvidhya.com/blog/2021/02/a-simple-guide-to-metrics-for-calculating-string-similarity/
# https://en.wikipedia.org/wiki/Levenshtein_distance
# https://github.com/explosion/spaCy/blob/master/spacy/glossary.py
#  considerar caminhos que tenham labels adequados, considerar caminhos bidirecionais
# https://medium.com/@dhartidhami/understanding-bert-word-embeddings-7dc4d2ea54ca
#  usar o bert pra saber se os camihos são relevantes ou não

def find_entities(entity_given: str, dict_dependencies: dict)-> list:
    if entity_given in dict_dependencies:
        entity_found = [entity_given]
        return entity_found

    else:
        entity_found = []
        temp = list(dict_dependencies)
        for k, v in dict_dependencies.items():
            if entity_given in k and k not in entity_found:
                entity_found.append(k)

        if not entity_found:
            possible_entities = []
            x = entity_given.split()
            print(f"x: {x}")
            for entity in x:
                if x.index(entity) < len(x)-1:
                    entity_2 = x[x.index(entity)+1]
                    print(f"entity: {entity}")
                    print(f"entity_2: {entity_2}")
                    
                    for key,value in dict_dependencies.items():
                        print(f"key: {key}")
                        key_list = key.split()
                        if len(key_list) > 1:
                            for k_key in key_list:
                                if key_list.index(k_key) < len(key_list)-1:
                                    k_key_2 = key_list[key_list.index(k_key) + 1]
                                    print(f"k_key: {k_key}")
                                    print(f"k_key_2: {k_key_2}")
                                    if entity in k_key and entity_2 in k_key_2 and key not in entity_found and key not in stop_words:
                                        print(f"Adding {key}")
                                        possible_entities.append(key)
                        else:
                            if temp.index(key) < len(temp)-1:
                                key_2 = temp[temp.index(key) + 1]
                                print(f"key_2: {key_2}")
                                if entity in key and entity_2 in key_2 and key not in entity_found and key not in stop_words:
                                    print(f"Adding {key}")
                                    possible_entities.append(key)
            entity_found = possible_entities

            return entity_found

enti = find_entities("Asian Spirit and Zest Air", dict_dependencies)

print(enti)