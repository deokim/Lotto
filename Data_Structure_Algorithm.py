# Bubble Sort

def bubble_sort(List):
    
    unsorted_until_index=len(List)-1
    sorted=False

    while not sorted:
        sorted=True
        for i in range(unsorted_until_index):
            if List[i] > List[i+1]:
                sorted=False
                List[i],List[i+1] = List[i+1], List[i]

        unsorted_until_index -=1

    return List

List=[65,66,45,35,25,10,15]
bubble_sort(List)
print(List)


#Selection Sort
def selection_sort(List):
    unsorted_until_index=len(List)-1
        
    for i in range(unsorted_until_index):
        lowest_index=i
        for j in range(i+1, unsorted_until_index+1):
            if List[lowest_index] > List[j]:
                lowest_index=j

        if lowest_index != i:
            List[i],List[lowest_index] = List[lowest_index], List[i]
    
    return List

List=[65,66,45,35,25,10,15]
selection_sort(List)
print(List)





########### Linter
stacks=[]
open_brace=["(","[","{"]
close_brace=[")","]","}"]
brace_pair={")":"(", "]":"[", "}":"{"}

def lint(text):
    for char in text:
        if opening_brace(char):
            stacks.append(char)
        elif closing_brace(char):
            if brace_pair[char] ==stacks[len(stacks)-1]:
                stacks.pop()
            else:
                print(f"Incorrect closing brace:{char}")
        
    if len(stacks) >0 :
        print(f"{stacks[len(stacks)-1]} does not have a closing brace")

def opening_brace(char):
    if char in open_brace:
        return True

def closing_brace(char):
    if char in close_brace:
        return True

lint("( var x ={ y:[1,2,3] ) }")
