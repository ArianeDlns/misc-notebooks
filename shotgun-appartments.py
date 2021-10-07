#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 15:00:01 2018

@author: ariane
"""

import numpy as np
import random
import matplotlib
import matplotlib.pyplot as plt
import math
import xlrd
from collections import Iterable


N = 20

# p est la proba qu'un individu soit muté
# q est la proba qu'un gène soit muté
p = 0.5
q = 0.2

#Taille de la population créée
Taille = 20

#Nombre de générations créées
NB_Gen = 10000

Gens = xlrd.open_workbook("appart.xlsx").sheet_by_index(0)
Colloc=[Gens.cell(0,i).value for i in [i for i in range(1,19)]]

Tab =[[Gens.cell(j,i).value for i in [i for i in range(1,19)]] for j in [i for i in range(1,19)] ]
      
n=10000 

def cout(L):
    s=0
    for i in range(len(L)):
        for j in range(len(L)):
            s+=Tab[L[j]][L[i]]
    return s
    
def inL(e, L):
    if e == L: return True
    if isinstance(L, Iterable):
        for l in L:
            if inL(e, l): return True
    return False
    
def creer_population():
    Pop =[[],[],[]]
    while len(Pop[0])<6 :
        a=random.randint(0,len(Colloc)-1)
        if not(inL(a, Pop)) :
            Pop[0]+=[a]
    while len(Pop[1])<6 :
        a=random.randint(0,len(Colloc)-1)
        if not(inL(a, Pop)):
            Pop[1]+=[a]
    while len(Pop[2])<6 :
        a=random.randint(0,len(Colloc)-1)
        if not(inL(a, Pop)) :
            Pop[2]+=[a]
    return Pop
    
def Eval(pop):
    return cout(pop[0])+cout(pop[1])+cout(pop[2])

def nom_appart(BestAppart):
    A1,A2,A3=[],[],[]
    for i in range(6):
        A1+=[Colloc[BestAppart[0][i]]]
        A2+=[Colloc[BestAppart[1][i]]]
        A3+=[Colloc[BestAppart[2][i]]]
    print(A1)
    print(A2)
    print(A3)
    return 

# Tri par tas
def ajout(x,T):
    n = len(T)
    T.append(x)
    i = n
    
    while i > 0 and T[i][1] > T[(i-1)//2][1]:
        T[i],T[(i-1)//2] = T[(i-1)//2],T[i]
        i = (i-1)//2

def mise_en_tas(l):
    T = []
    
    for x in l:
        ajout(x,T)
    
    return(T)

def reconstituer(T,n):
    i = 0
    
    while i < n:
        if 2*i + 2 <= n:
            g,d = T[2*i + 1][1],T[2*i + 2][1]
            if T[i][1] < max(g,d):
                if d < g:
                    T[i],T[2*i + 1] = T[2*i + 1],T[i]
                    i = 2*i + 1
                else:
                    T[i],T[2*i + 2] = T[2*i + 2],T[i]
                    i = 2*i + 2
            else: i = n
        elif 2*i + 1 <= n:
            if T[i][1] < T[2*i + 1][1]:
                 T[i],T[2*i + 1] = T[2*i + 1],T[i]
                 i = 2*i + 1
            else: i = n
        else: i = n
    
    return(T)

def heapsort(T):
    T = mise_en_tas(T)
    n = len(T)
    
    for i in range(1,n):
        T[0],T[n-i] = T[n-i],T[0]
        reconstituer(T,n-1-i)
    
    return(T)
    
def eval_pop(Pop):
    Eval = []
    
    for i in range(Taille):
        Eval.append([i,Eval(Pop[i])])
    return Eval


def tri(Eval):
    return heapsort(Eval)

def new_pop(Pop): # étape de sélection et croisement
    Eval = tri(eval_pop(Pop))
    Next_gen = []
    
    for i in range(Taille//2):  #on prend les Taille/ 2 meilleurs
        Next_gen.append(Pop[Eval[i][0]])
    for i in range(Taille//2):
        j = random.randint(0,Taille//2-1)
        k = random.randint(0,Taille//2-1)
        l1 = Pop[Eval[j][0]][0:N//2]
        l2 = Pop[Eval[k][0]][N//2:N]
        New_ind = np.concatenate((l1,l2))
        Next_gen.append(New_ind)
    
    return Next_gen

#Tous les individus peuvent être mutés sauf le meilleur
def mutation(Pop):
    
    for i in range(1,Taille):
        if random.random() < p:
            for j in range(1,N-1):
                if random.random() < q:
                    Pop[i][j] = random.randint(0,2)
    
    return Pop

def fonction_finale():
    Pop = creer_population()
    
    for i in range(NB_Gen):
        Pop = new_pop(Pop)
        Pop = mutation(Pop)
    Eval = tri(eval_pop(Pop))
    
    return Pop[Eval[0][0]],Eval[0][1]
    

def Best():
    M=0
    for i in range(n):
        Appart=creer_population()
        if Eval(Appart)>M :
            M=Eval(Appart)
            BestAppart=Appart
    return(nom_appart(BestAppart))
    
Best()
