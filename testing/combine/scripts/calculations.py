from scripts.charts import *

TYPECHART = getTypeChart()


def experience(current_level, experience_group = 'slow'):
    required_exp = 0
    n = current_level
    if experience_group == 'slow':
        required_exp = 1.25 * n ** 3
    elif experience_group == 'medium slow':
        required_exp = 6/5 * n ** 3 - 15* n **2 +100 * n - 140
    elif experience_group == 'medium fast':
        required_exp = n ** 3
    elif experience_group == 'fast':
        required_exp = 0.8 * n ** 3
    elif experience_group == 'erratic':
        if n  <= 50:
            required_exp = n**3 * (100 - n)/50
        elif 50 < n <= 68:
            required_exp = n**3 * (150 - n)/50
        elif 68 < n <= 98:
            required_exp = n**3 * (1911 - 10 * n)/1500
        elif 98 < n <= 100:
            required_exp = n**3 * (160 - n)/100
    
    if n == 100:
        required_exp = 0

    return required_exp
        
#-------------------------------------------------------------------------------

def damageCalc(target, projectile):
    ''' 
    PURPOSE:
    Calculate the damage inflicted by a projectile on a target
    '''
    base_damage = projectile.dmg
    weakness_multiplier = TYPECHART[projectile.type][target.type.upper()]
    return base_damage * weakness_multiplier





