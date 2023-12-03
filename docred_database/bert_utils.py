from functions_bert import sentence_transformer, bert_resume
from transformers import logging

logging.set_verbosity_error()

relations = {
    "P6": "head of government",
    "P17": "country",
    "P19": "place of birth",
    "P20": "place of death",
    "P22": "father",
    "P25": "mother",
    "P26": "spouse",
    "P27": "country of citizenship",
    "P30": "continent",
    "P31": "instance of",
    "P35": "head of state",
    "P36": "capital",
    "P37": "official language",
    "P39": "position held",
    "P40": "child",
    "P50": "author",
    "P54": "member of sports team",
    "P57": "director",
    "P58": "screenwriter",
    "P69": "educated at",
    "P86": "composer",
    "P102": "member of political party",
    "P108": "employer",
    "P112": "founded by",
    "P118": "league",
    "P123": "publisher",
    "P127": "owned by",
    "P131": "located in the administrative territorial entity",
    "P136": "genre",
    "P137": "operator",
    "P140": "religion",
    "P150": "contains administrative territorial entity",
    "P155": "follows",
    "P156": "followed by",
    "P159": "headquarters location",
    "P161": "cast member",
    "P162": "producer",
    "P166": "award received",
    "P170": "creator",
    "P171": "parent taxon",
    "P172": "ethnic group",
    "P175": "performer",
    "P176": "manufacturer",
    "P178": "developer",
    "P179": "series",
    "P190": "sister city",
    "P194": "legislative body",
    "P205": "basin country",
    "P206": "located in or next to body of water",
    "P241": "military branch",
    "P264": "record label",
    "P272": "production company",
    "P276": "location",
    "P279": "subclass of",
    "P355": "subsidiary",
    "P361": "part of",
    "P364": "original language of work",
    "P400": "platform",
    "P403": "mouth of the watercourse",
    "P449": "original network",
    "P463": "member of",
    "P488": "chairperson",
    "P495": "country of origin",
    "P527": "has part",
    "P551": "residence",
    "P569": "date of birth",
    "P570": "date of death",
    "P571": "inception",
    "P576": "dissolved, abolished or demolished",
    "P577": "publication date",
    "P580": "start time",
    "P582": "end time",
    "P585": "point in time",
    "P607": "conflict",
    "P674": "characters",
    "P676": "lyrics by",
    "P706": "located on terrain feature",
    "P710": "participant",
    "P737": "influenced by",
    "P740": "location of formation",
    "P749": "parent organization",
    "P800": "notable work",
    "P807": "separated from",
    "P840": "narrative location",
    "P937": "work location",
    "P1001": "applies to jurisdiction",
    "P1056": "product or material produced",
    "P1198": "unemployment rate",
    "P1336": "territory claimed by",
    "P1344": "participant of",
    "P1365": "replaces",
    "P1366": "replaced by",
    "P1376": "capital of",
    "P1412": "languages spoken, written or signed",
    "P1441": "present in work",
    "P3373": "sibling"
}

possible_relations = {
    "direct": {
        "P6": ["is the head of government of", "is the president of", "is the primer ministry of", "is the king of"],
        "P17": ["is located in the country"], 
        "P19": ["is the birthplace of"], 
        "P20": ["is the place of death of"], 
        "P22": ["is the father of"], 
        "P25": ["is the mother of"], 
        "P26": ["is the spouse of", "is married to"], 
        # "P27": ["is the country of citizenship of", "is"], # geralmente conecta nome da pessoa e nacionalidade como british, canadian e etc
        # "P30": "is the continent of", # uma das entidades é um continente
        # "P31": "has an instance of", # depende de conhecimento sobre as entidades, não fica explícito na frase 
        "P35": ["is the head of state of"], 
        "P36": ["is the capital of"],
        # "P37": ["is the official language of"], #depende de conhecimento das entidades, não fica explicito na frase
        "P39": ["is a position held by"], 
        "P40": ["is the child of", "is the daughter of", "is the son of"],
        "P50": ["is the author of"], 
        # "P54": ["is the member of sports team"], # depende do entendimento de que uma das entidades é um time, cabe na relação P108
        "P57": ["is the director of"], 
        "P58": ["is the screenwriter of", "wrote", "has written"], 
        "P69": ["was educated at", "studied at"], 
        "P86": ["is the composer of"], 
        # "P102": ["is the member of political party"], # depende do entendimento de que uma das entidades é um partido, cabe na relação P108
        "P108": ["is the employer of"], 
        "P112": ["was founded by"], 
        "P118": ["is the league of"], 
        "P123": ["is the publisher of"], 
        "P127": ["is owned by"], 
        "P131": ["is located in the administrative territorial entity of"], 
        # "P136": ["is the genre of"], # exige um pré conhecimento de que uma das entidades é um gênero musical
        "P137": ["is the operator of"], 
        "P140": ["is the religion of", "is the church of"], 
        "P150": ["contains administrative territorial entity of"], 
        "P155": ["follows"], 
        "P156": ["is followed by"], 
        # "P159": ["has headquarters location in"],
        "P161": ["is a cast member of"], 
        "P162": ["is the producer of"], 
        "P166": ["is the award received by"], 
        "P170": ["is the creator of"], 
        # "P171": ["is the parent taxon of"], 
        # "P172": ["is the ethnic group from"], 
        "P175": ["is the performer of"], 
        "P176": ["is the manufacturer of"], 
        "P178": ["is the developer of"],
        "P179": ["is a series from"], 
        # "P190": ["is the sister city of"], 
        # "P194": ["is the legislative body of"], 
        "P205": ["is the basin country of"], 
        "P206": ["is located in or next to body of water of"],
        "P241": ["had served in", "served in"], 
        "P264": ["was released by record label"], 
        "P272": ["was released by"], 
        "P276": ["is the location of"], 
        # "P279": ["is a subclass of"],
        "P355": ["is the subsidiary of", "is the owner of"], 
        "P361": ["is part of"], 
        # "P364": ["is the original language of work of"], 
        "P400": ["is run on", "is released for platform"], 
        "P403": ["is the mouth of the watercourse of"],
        "P449": ["is the original network of"], 
        "P463": ["is member of"], 
        "P488": ["is chairman of", "is chairwoman of"], 
        "P495": ["is the country of origin of"], 
        "P527": ["has part of"], 
        "P551": ["is the residence of"], 
        "P569": ["was born on"], 
        "P570": ["died on", "died in"], 
        "P571": ["is the beginning of"], 
        "P576": ["was dissolved at", "was abolished at", "was demolished at"], 
        "P577": ["is the publication date of"], 
        "P580": ["is the start time of"], 
        "P582": ["is the end time of"], 
        # "P585": ["is the point in time of"], 
        "P607": ["is a conflict that envolved"], 
        "P674": ["is characters of"], 
        "P676": ["has lyrics by"], 
        "P706": ["is located on terrain feature on"], 
        "P710": ["is a participant of"], 
        "P737": ["was influenced by"], 
        "P740": ["is the location of formation of"], 
        "P749": ["is a parent organization of"], 
        "P800": ["is a notable work of"], 
        # "P807": ["was separated from"], 
        "P840": ["is the narrative location of"], 
        "P937": ["is the work location of"], 
        "P1001": ["applies to jurisdiction on"], 
        "P1056": ["is the product of", "is the material produced by"], 
        "P1198": ["is the unemployment rate of"], 
        "P1336": ["is a territory claimed by"], 
        "P1344": ["is the participant of"], 
        "P1365": ["replaces"], 
        "P1366": ["was replaced by"], 
        "P1376": ["has as capital"], 
        "P1412": ["are the languages spoken, written or signed by"], 
        "P1441": ["is present in work of"], 
        "P3373": ["is sibling of"],
    }, 
    "inverse": {
        "P6": ["is ruled by"],
        "P17": ["is the country of"], 
        "P19": ["was born in"], 
        "P20": ["died in"],
        # "P27": "is a citizen of",
        # "P30": "has as continent", uma das entidades é um continente
        # "P31": "is an instance of",
        "P36": ["has as capital"], 
        # "P37": ["has as official language"],
        "P39": ["holds the position of"],
        "P50": ["is authored by"],
        # "P54": ["is starter of"], 
        "P57": ["is directed by"], 
        "P58": ["was written by"], 
        "P69": ["is the education place from"],
        "P86": ["was composed by"], 
        # "P102": ["has as member of political party"], 
        "P108": ["is the employee of", "works at"], 
        "P112": ["is the founder of"], 
        "P118": ["has as league"],
        "P123": ["was published by"], 
        "P127": ["is the owner of"], 
        "P131": ["was the location in the administrative territorial entity of"], 
        # "P136": ["has as genre of"], 
        "P137": ["is operated by"], 
        "P140": ["has as religion"],
        "P150": ["was the location in the administrative territorial entity of"], 
        # "P159": ["is the headquarters location of"],
        "P161": ["has as a cast member"],
        "P166": ["received the award of"],
        "P170": ["was created by"],
        # "P171": ["is the parent taxon of"],
        # "P172": ["has as ethnic group"], 
        "P175": ["is performed by"], 
        "P176": ["is manufactured by"], 
        "P178": ["is developed by"], 
        "P179": ["has as series"], 
        # "P194": ["has as legislative body of"], 
        "P205": ["has as basin country the"], 
        "P206": ["is the location in or next to body of water of"],
        # "P241": [""], 
        "P264": ["released the album"], 
        "P272": ["released", "produced"], 
        "P276": ["was located in"], 
        # "P279": ["has as subclass"],
        "P355": ["is subsidized by", "owned by"],
        # "P364": ["has as original language of work"], 
        "P400": ["platform runs", "runs"],
        "P403": ["has as mouth of the watercourse"],
        "P449": ["has as original network"], 
        "P463": ["has as member"], 
        "P488": ["has as chairman", "has as chairwoman"], 
        "P495": ["is from country of origin"], 
        "P527": ["is part of"], 
        "P551": ["live-in"], 
        "P569": ["was born on the date"], 
        "P570": ["was dead on the date"], 
        "P571": ["starts at"],
        "P576": ["dissolved the", "abolished the", "demolished the"], 
        "P577": ["was published on"], 
        "P580": ["began in"], 
        "P582": ["ended in"], 
        # "P585": ["has as point in time"], 
        "P607": ["were envolved in the conflict"], 
        "P674": ["has the characters"], 
        "P676": ["wrote the lyrics of"], 
        "P706": ["has as location on terrain feature on"],
        "P710": ["has as participant of"], 
        "P737": ["influenced"], 
        "P740": ["was formed in"], 
        "P749": ["has as parent organization"], 
        "P800": ["has as notable work"], 
        "P840": ["has as narrative location"], 
        "P937": ["has as work location"], 
        "P1001": ["was applied to jurisdiction on"],
        "P1198": ["has unemployment rate"], 
        "P1336": ["is claimed as territory"], 
        "P1344": ["has as participant"], 
        "P1412": ["speak, write or sign the languages"], 
        "P1441": ["has present in work"],
    }
}


def selection_by_bert_resume(paragraph: str, path: str, entity_0: str, entity_1: str):

    created_relations = []
    for k,v in possible_relations.items():
        for relation_id, list_relation in v.items():
            for relation in list_relation:
                created_relation = entity_0 + " " + relation + " " + entity_1
                cos_diff = bert_resume(paragraph, path, created_relation)
                created_relations.append({"relation_id": relation_id, "created_relation": created_relation, "similarity": cos_diff, "k": k})

    max_tensor = 0
    id = 0
    relation = ""
    for item in created_relations:
        if item.get("similarity") > max_tensor:
            id = item.get("relation_id")
            relation = item.get("created_relation")
            max_tensor = item.get("similarity")
            way = item.get("k")

    rel = relations.get(id)

    print(f"Relation found by bert resume: id {id, rel}, relation {relation}, similarity {max_tensor}, way {k}")

    return id, relation, k, rel


def selection_by_bert_sc(entity_0: str, entity_1: str, sent: str):

    created_relations = []
    for k,v in possible_relations.items():
        for relation_id, list_relation in v.items():
            for relation in list_relation:
                created_relation = f"{entity_0} {relation} {entity_1}"
                sentence_transformer_c = sentence_transformer(sent, created_relation)
                created_relations.append({"relation_id": relation_id, "created_relation": created_relation, "similarity": sentence_transformer_c[0].item(), "k": k})

    max_tensor = 0
    id = 0
    relation = ""
    for item in created_relations:
        if item.get("similarity") > max_tensor:
            id = item.get("relation_id")
            relation = item.get("created_relation")
            max_tensor = item.get("similarity")
            way = item.get("k")

    rel = relations.get(id)

    print(f"Relation found by bert: id {id, rel}, relation {relation}, similarity {max_tensor}, way {k}")

    return id, relation, k, rel


def subproperties(relation_id: int)-> list:

    properties_and_subproperties = {
        "P6": ["P35"],
        "P17": ["P131", "P27"],
        "P19": ["P27"],
        "P22": ["P40"],
        "P25": ["P40"],
        "P27": ["P19"],
        "P30": ["P150", "P361"],
        "P35": ["P27", "P6"],
        "P36": ["P1376"],
        "P39": ["P527"],
        "P40": ["P22", "P25"],
        "P50": ["P170", "P800", "P58"],
        "P54": ["P108"],
        "P58": ["P50"],
        "P86": ["P676"],
        "P102": ["P108"],
        "P108": ["P54", "P102"],
        "P112": ["P108"],
        "P127": ["P355"],
        "P131": ["P17", "P1001", "P150", "P706"],
        "P150": ["P17", "P131"],
        "P155": ["P156"],
        "P156": ["P155"],
        "P159": ["P131", "P276", "P17"],
        "P162": ["P175", "P1056"],
        # "P170": ["P50"],
        "P172": ["P27"],
        "P175": ["P170"],
        "P176": ["P178"],
        "P179": ["P361", "P279"],
        "P194": ["P1001", "P131", "P17"],
        "P205": ["P17", "P131"],
        "P206": ["P131"],
        "P264": ["P272"],
        "P272": ["P449", "P264"],
        "P276": ["P131", "P159"],
        "P355": ["P749", "P127", "P361"],
        "P361": ["P527", "P355"],
        "P364": ["P495"],
        "P400": ["P178"],
        "P463": ["P527", "P150", "P131", "P17"],
        "P488": ["P102", ],
        "P495": ["P17"],
        "P527": ["P179", "P30", "P361"],
        "P551": ["P19", "P27"],
        "P580": ["P582", "P585"],
        "P582": ["P580", "P585"],
        "P585": ["P580", "P582"],
        "P674": ["P1441"],
        "P676": ["P86"],
        "P706": ["P206", "P131"],
        "P740": ["P17", "P159", "P131"],
        "P749": ["P127", "P355"],
        "P800": ["P170", "P50"],
        "P937": ["P551"],
        "P1001": ["P131", "P17"],
        "P1056": ["P178", "P137", "P176", "P1056"],
        "P1336": ["P150"],
        "P1344": ["P710"],
        "P1365": ["P1366"],
        "P1366": ["P1365"],
        "P1376": ["P17", "P131", "P150", "P36"],
        "P1441": ["P674"],
    }

    subproperties = properties_and_subproperties.get(relation_id, [])

    return subproperties