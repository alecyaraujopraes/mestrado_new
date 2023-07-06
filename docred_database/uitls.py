import pandas as pd
from Levenshtein import jaro_winkler

def compare_strings(str1: str, str2: str):
    for Entidade_0, Entidade_1, Relacao_encontrada in zip(df_spacy_selected.Entidade_0, df_spacy_selected.Entidade_1, df_spacy_selected.Relacao_encontrada):
        if (jaro_winkler(entity_tail, Entidade_0)> 0.7 or jaro_winkler(entity_tail, Entidade_1)>0.7) and (jaro_winkler(entity_head, Entidade_0)> 0.7 or jaro_winkler(entity_head, Entidade_1)>0.7):
            print(f"Frase: {sent}")
            print(f"Entidades: {entity_tail, entity_head, Entidade_0, Entidade_1, relation, Relacao_encontrada}")
        else:
            print(f"No entities")