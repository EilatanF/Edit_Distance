#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import sys

#memoize hint: http://www.python-course.eu/python3_memoization.php

def memoize(f):
  memo = {} # use dictionary
  def helper(wordI, wordJ):
    key = wordI + " " + wordJ
    if key not in memo:
      memo[key] = f(wordI, wordJ)
    return memo[key]
  return helper

@memoize
def levenshtein(wordI, wordJ):
  i = len(wordI)
  j = len(wordJ)
  dist = 1
  if i == 0:
    dist = j
  elif j == 0:
    dist = i
  else:
    lev1 = levenshtein(wordI[:-1], wordJ) + 1
    lev2 = levenshtein(wordI, wordJ[:-1]) + 1
    lev3 = levenshtein(wordI[:-1], wordJ[:-1])

    if wordI[-1:] != wordJ[-1:]:
      lev3 = lev3 + 2

    dist = min(lev1, lev2, lev3)
  
  return dist

@memoize
def transpose(wordI, wordJ):
  i = len(wordI)
  j = len(wordJ)
  dist = 0
  if i == 0:
    dist = j
  elif j == 0:
    dist = i
  else:
    tra1 = transpose(wordI[:-1], wordJ) + 1
    tra2 = transpose(wordI, wordJ[:-1]) + 1
    tra3 = transpose(wordI[:-1], wordJ[:-1])
    tra4 = tra1 + 1

    if wordI[-1:] != wordJ[-1:]:
      tra3 = tra3 + 2
      
    if i > 1 and j > 1 and wordI[-2:-1] == wordJ[-1:] and wordI[-1:] == wordJ[-2:-1]:
      tra4 = transpose(wordI[:-2], wordJ[:-2]) + 1

    dist = min(tra1, tra2, tra3, tra4)
    
  return dist

mode = int(sys.argv[1])
infile = sys.argv[2]
dictionary = sys.argv[3]
output = sys.argv[4]

di = open(dictionary, "r")
dic = di.read()
dict = re.split("\n+", dic)

ra = open(infile, "r")
raw = ra.read()
entries = re.split("\n+", raw)

ou = open(output, "w+")

for wI in entries:
  currDist = 100  
  currWord = ''
  lenI = len(wI)
  
  for wJ in dict:
    lenJ = len(wJ) 
    dist = abs(lenI-lenJ)
    
    if (dist <= currDist):
      if mode == 1:
        dist = levenshtein(wI, wJ)
      elif mode == 2:
        dist = transpose(wI, wJ)
    
    if (dist < currDist):
      currDist = dist
      currWord = wJ
      
  writeWord = currWord + ' ' + str(currDist) + '\n'
  ou.write(writeWord)
  
di.close()
ra.close()
ou.close()