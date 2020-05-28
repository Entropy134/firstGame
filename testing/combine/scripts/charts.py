import pandas as pd

def getTypeChart():
    '''
    PURPOSE:
    Return a chart of type weaknesses.

    TYPECHART = {'ATTACKER' : {'DEFENDER': MULTIPLIER}}
    '''
    TYPECHART = {
        'FIRE' :{'FIRE': 0.5, 'GRASS':2.0, 'WATER':0.5},
        'GRASS':{'FIRE': 0.5, 'GRASS':0.5, 'WATER':2.0},
        'WATER':{'FIRE': 2.0, 'GRASS':0.5, 'WATER':0.5},
        }
    return TYPECHART

def getPokemonStats(specifiedPokemon):
    FILE = 'assets/pokemon.csv'
    df = pd.read_csv(FILE)
    df = df.loc[(df['Name'].str.contains('Mega')==False)&\
        (df['Name'].str.contains('Primal')==False)]
    
    df.set_index("Name", inplace = True)
    
    return df.loc[specifiedPokemon]
    

