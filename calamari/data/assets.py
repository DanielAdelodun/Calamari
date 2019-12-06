import krakenex

kraken = krakenex.API()

def filterDuplicates(asset_pair):
    """Filter function used to remove duplicate entries in the :data:`asset_pairs` list"""
    if 'd' in asset_pair:
        return False
    else:
        return True

def get_assets():
    """Returns a list of all availible :data:`assets`"""
    assets_result = kraken.query_public('Assets')
    assets_info = assets_result['result']
    assets = [asset for asset in assets_info]
    return assets
        
# Returns either a simple list of all Pair names,
# Or a dictionary. Pair names are the keys and information on the Pairs the values.
def get_asset_pairs(info=True):
    """Returns either a list of all :data:`asset_pairs`, or a dictionary of :data:`all_pairs_info`.

    Args:
      info (bool): With or without info.

    Returns:
      asset_pairs (list): List of asset pairs. or 
      asset_pairs_info (dict): Dict of asset pairs and information.

    """
    asset_pairs_result = kraken.query_public('AssetPairs')
    asset_pairs_info = asset_pairs_result['result']
    asset_pairs = [asset_pair for asset_pair in asset_pairs_info]
    asset_pairs = list(filter(filterDuplicates, asset_pairs))  # Remove weird pairs that end with a '.d'.
    return asset_pairs_info if info else asset_pairs
