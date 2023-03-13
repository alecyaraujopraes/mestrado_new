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

    def build_path(l:list, v:list)->list:
        for item in v:
            l.append(item)
            if item in dependencies:
                v = dependencies.get(f"{item}")
                if v:
                    build_path(l, v)
                else:
                    return l


    for k, v in dependencies.items():
        l = []
        l.append(k)
        build_path(l, v)
        print(l)

l(dict_dependencies)
        
    
    


