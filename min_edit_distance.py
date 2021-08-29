# -*- coding: utf-8 -*-
"""
@author: ryan.shea
"""
import numpy as np

with open("edit_dist_data.txt", encoding='utf8') as inp:
    lines=inp.readlines()

eng=[]
oth=[]

for l in lines:
    
    l = l.strip().split('|||')
    eng.append(l[0].strip())
    oth.append(l[1].strip())

# edit distance algorithm with backtracing

sub_cost= lambda a,b: 0 if a==b else 1

up='^'
left='<'
diag='\\'

def edit_dist_matrix_backtrace(source,target):

    m=len(source)+1
    n=len(target)+1
    
    d=[[0 for i in range(n)] for j in range(m)]
    p=[[0 for i in range(n)] for j in range(m)]
    
    for i in range(1, n):
        d[0][i]=d[0][i-1]+1
        p[0][i]=left
    for j in range(1,m):
        d[j][0]=d[j-1][0]+1
        p[j][0]=up
    
    for i in range(1,m):
        for j in range(1,n):
            left_val=d[i][j-1]+1
            up_val=d[i-1][j]+1
            diag_val=d[i-1][j-1]+sub_cost(source[i-1], target[j-1])
            direction=[]
            minimum=min(left_val, up_val, diag_val)
            if diag_val==minimum: direction.append(diag)
            if up_val==minimum: direction.append(up)
            if left_val==minimum: direction.append(left)
            
            
            d[i][j]=minimum
            p[i][j]=direction
            
    return p,d

dir_array=edit_dist_matrix_backtrace('intention', 'execution')[0]
dist_array=edit_dist_matrix_backtrace('intention', 'execution')[1]

dir_array_np=np.array(dir_array)


def backtrace_driver(d):
    return backtrace_recur(d, len(d)-1, len(d[0])-1, [])

def backtrace_recur(d, i, j, path):
    path.append([i,j])
    if i==0 or j==0:
        return path
    
    if diag in d[i][j]:
        return backtrace_recur(d, i-1, j-1, path)
    if left in d[i][j]:
        return backtrace_recur(d, i, j-1, path)
    if up in d[i][j]:
        return backtrace_recur(d, i-1, j, path)

recur_test=backtrace_driver(dir_array)


#get pointer array for word pair
word_pointers=edit_dist_matrix_backtrace('intention','execution')[0]
#get index sequence
word_path=backtrace_driver(word_pointers)


# find common letters inserted

def get_letter_freq(source, target, path_list, letters_arg):
    letters=letters_arg
    prev_i=path_list[0][0]
    prev_j=path_list[0][1]
    for i in range(1,len(path_list)):
        if path_list[i][0]==prev_i and path_list[i][1] == prev_j-1:
            char=target[path_list[i][1]]
            added=False
            for e in range(len(letters)):
                if letters[e][0] == char:
                    letters[e][1]+=1
                    added=True
            if not added:
                letters.append([char, 1])
                
        prev_i=path_list[i][0]
        prev_j=path_list[i][1]
            
    return letters

def get_inserted_letters(source,target,letters):
    dir_array=edit_dist_matrix_backtrace(source, target)[0]
    path_list=backtrace_driver(dir_array)
    
    
    return get_letter_freq(source, target, path_list, letters)

def get_all_insert_letters(lang1,lang2):
    result=[]
    for i in range(len(lang1)):
        result=get_inserted_letters(lang1[i],lang2[i], result)
    return result




letter_insertions=get_all_insert_letters(eng, oth)




