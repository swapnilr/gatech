#Consider an arbitrary string X = x_1...x_n.  
#A subsequence of X is a string of the form 
#x_i_1 x_i_2...x_i_k ,where 1 <= i_1< ... < i_k <= n.  
#A string is palindromic if it is equal to its 
#own reverse (i.e. the string is the same whether 
#read backwards or forwards).  

#a) Derive a recurrence for L(i, j). Why is your recurrence correct?
#   L(i,j) = L(i+1, j-1) + 2 if i == j else max(L(i, j-1), L(i+1, j)
#   if x_i==x_j
#     L(i,j) = L(i+1, j-1) + 2
#   else
#     L(i,j) = max(L(i, j-1), L(i+i, j))
#b) What is the base case?
#   if i == j: L(i,j) = 1
#   if i > j: L(i,j) = 0
#c) Use dynamic programming to implement the procedure below.
#d) What is its running time?
#   O(n^2)

def lps(s):
    """Returns a longest palindromic subsequence of the string s."""
    return iterative_lps(s)

def iterative_lps(s):
    """Returns a longest palindromic subsequence of the string s."""
    table2 = []
    for i in range(len(s)):
        table2.append([])
        for j in range(len(s)):
            table2[i].append(-1)
    
    for i in range(len(table2)):
        table2[i][i] = 1
    
    for size in range(2, len(s) + 1):
        for i in range(len(s) + 1 - size):
            j = i + size - 1
            if s[i] == s[j]:
                add = 0 if size == 2 else table2[i+1][j-1]
                table2[i][j] = 2 + add
            else:
               table2[i][j] = max(table2[i][j-1], table2[i+1][j])    
    p = ""
    i, j = 0, len(s) - 1
    added = False
    while j >= i:
        if i == j:
            added = True
            p = p + s[i]
            break
        else:
            if s[i] == s[j]:
                p = p + s[i]
                i = i+1
                j = j-1
            elif table2[i][j-1] == table2[i][j]:
                j= j-1
            elif table2[i+1][j] == table2[i][j]:
                i = i+1
            else:
                assert(False)
    if added:
        p = p + p[:-1][::-1]
    else:
        p = p + p[::-1]
    return p

def recursive_lps(s):
    """Returns a longest palindromic subsequence of the string s."""
    table = []
    for i in range(len(s)):
        table.append([])
        for j in range(len(s)):
            table[i].append(-1)
    
    # This function does any work only O(n^2) times, as the if check at the beginning
    # prevents any repeated work more than once per i,j pair
    def helper(i,j):
        if table[i][j] != -1:
            return table[i][j]
        elif i==j:
            table[i][j] = 1
            return table[i][j]
        elif i > j:
            table[i][j] = 0
            return table[i][j]
        elif s[i] == s[j]:
            table[i][j] = helper(i+1, j-1) + 2
            return table[i][j]
        else:
            first = helper(i, j-1)
            second = helper(i+1, j)
            table[i][j] = max(first, second)
            return table[i][j]
    
    helper(0, len(s) - 1)
    
    # Since i starts at 0, and j at n - 1, and in each call either i increases by 1
    # or j decreases by 1, and we stop when i >= j, that means this function is called
    # at most n/2 times
    def backtrack(i, j):
        if i > j:
            return ""
        elif i == j:
            return s[i]
        else:
            if s[i] == s[j]:
                return s[i] + backtrack(i+1, j-1) + s[j]
            if table[i][j-1] == table[i][j]:
                return backtrack(i, j-1)
            elif table[i+1][j] == table[i][j]:
                return backtrack(i+1, j)
            else:
                assert(False)

    return backtrack(0, len(s) - 1)
            
def main():
    assert(lps('axayyybaxca4baza') in ['aabacabaa','axayyyaxa', 'aabaxabaa'])
                                        
if __name__ == "__main__":
    main()



    

