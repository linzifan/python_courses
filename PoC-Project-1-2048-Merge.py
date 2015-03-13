"""
Merge function for 2048 game.
"""
# codeskopter link void
def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    def put_zero(lst):
        """
        Put all non-zero tiles towards the beginning of list.
        """
        lstb = []
        for i in range(0,len(lst)):
            if lst[i]!=0: 
                lstb.append(lst[i])
        if len(lstb)<len(lst):
            lstb.extend([0]*(len(lst)-len(lstb)))
        return lstb


    def combine_pair(lst):
        """
        Combine pairs of tiles.
        """
        for i in range(0,len(lst)-1):
            if lst[i]==lst[i+1]:
                lst[i] = lst[i]*2
                lst[i+1] = 0
        return lst

    list_1 = put_zero(line)
    list_2 = combine_pair(list_1)
    list_3 = put_zero(list_2)
    return list_3

print merge([4])

