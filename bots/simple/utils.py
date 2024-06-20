
def get_available_upgrades(upgrades, upgrade_type = 2):
    current_levels = {mine['mineId']: mine['currentLevel'] for mine in upgrades}
    available_upgrades = []
    for upgrade in upgrades:
        if upgrade.get('currentLevel', -1) == upgrade.get('maxLevel'):
            continue
        if upgrade['type'] == upgrade_type:
            upgrade['payback'] = upgrade['nextPrice'] / (upgrade['nextVolume'] / 8)
            upgrade.pop('description', None)
            dependency_id = upgrade.get('dependencyMineId')
            dependency_level = upgrade.get('dependencyMineLevel')
            if current_levels.get(dependency_id, 0) >= dependency_level:
                available_upgrades.append(upgrade)
    return available_upgrades

def get_sorted_upgrades(upgrades, upgrade_type = 2):
    sorted_upgrades = sorted(get_available_upgrades(upgrades, upgrade_type), 
                             key=lambda x: x['payback'])
    return sorted_upgrades[:10]
