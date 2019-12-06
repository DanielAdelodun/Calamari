def trader(loop):
    '''
    Find profitable Loops and exploit them.
    '''
    try:
        # Check forward direction.
        volumes = loop.calculate()
        if volumes[0][0] < volumes[0][-1]: # Checking if the volume of bitcoin at the end would be larger than at the start.
            loop.execute(0.01)
            return
        elif volumes[1][0] < volumes[1][-1]: # Ditto, but using market prices.
            loop.execute(0.01, market=True)
            return

        # Check reverse.
        volumes = loop.calculate(reverse=True)
        if volumes[0][0] < volumes[0][-1]:
            loop.execute(0.01, reverse=True)
            return
        elif volumes[1][0] < volumes[1][-1]:
            loop.execute(0.01, reverse=True, market=True)
            return
    except:
        raise
