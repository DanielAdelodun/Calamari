def get_fee():
    '''Allows you to update fee. Returns the fee.'''
   
    global fee  # This will be the trasaction fee - or I guess more specifically,
                # it's what we multiply each starting transaction amount by to account for the fee.
    try:
        fee = float(input('What is the transaction fee? (as a percentage): '))
    except:
        print("Input invalid. Please try again, or type '111' to use the default amount.")
        get_fee()
        return
   
    if fee == 111:
        fee = 0.9974
    else:
        fee = 1 - fee / 100
        return fee

fee = 0.9974
