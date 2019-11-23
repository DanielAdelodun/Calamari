import krakenex

kraken = krakenex.API()

def filterDuplicates(asset_pair):
    if 'd' in asset_pair:
        return False
    else:
        return True

def get_assets():
    assets_result = kraken.query_public('Assets')
    assets_info = assets_result['result']
    assets = [asset for asset in assets_info]
    return assets
        

def get_asset_pairs(info=True):
    asset_pairs_result = kraken.query_public('AssetPairs')
    asset_pairs_info = asset_pairs_result['result']
    asset_pairs = [asset_pair for asset_pair in asset_pairs_info]
    asset_pairs = list(filter(filterDuplicates, asset_pairs))
    return asset_pairs_info if info else asset_pairs

