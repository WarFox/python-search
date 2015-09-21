#!/usr/bin/python
import os, sys, getopt, fnmatch, re

#References
'''
* http://stackoverflow.com/questions/5141437/filtering-os-walk-dirs-and-files
'''

rootdir = "/"
keywords = open('input.txt', 'r').read().upper().split()
global_keysfound = set()
global_splitre = '=|,|\*|\n|<'

includes = ['*.xml','*.java','*.sql'] # for files only
excludes = ['build','.idea', 'dist', 'test', 'target'] # for dirs and files

# transform glob patterns to regular expressions
includes = r'|'.join([fnmatch.translate(x) for x in includes])
excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

'''
closure based counter
'''
def initCounter(x):
  counter = [x]
  def inc():
     counter[0] += 1
     return counter[0]
  return inc

def sortItems(items):
    return sorted(items, key=lambda item: (int(item.partition(' ')[0])
                                if item[0].isdigit() else float('inf'), item))

'''
prints the contents of set and a new line
'''
def prettyPrint(items):
    msg = ''
    delim = ''
    items = sortItems(items)
    for item in items:
        msg +=  (delim + item)
        delim = ' | '
    print msg
    return '\n'

'''
Function that searches for keywords in each file
'''
def search(filepath):
  global global_keysfound
  global global_splitre
  #open file for reading and get content as list
  f = open(filepath, "r")
  content = f.read().upper()
  #split content into whole words
  content = re.split(global_splitre, content )
  #print "searching ", f.name
  keysfound = set()
  found = False
  for key in keywords:
    found =  any(key in keywords for keywords in content)
    if found:
      keysfound.add(key)
  if found:
    print "\n", filepath
    prettyPrint(keysfound)
    global_keysfound = global_keysfound | keysfound


'''
Check if a filename pattern is okay for searching
If filename contains text from excludes list then return false
'''
def isFileNameOkay(filename):
  for exclude in excludes:
    filename = filename.upper()
    exclude = exclude.upper()
    found = exclude in filename
    #found = (filename.find(exclude) != -1)
    if found == True:
      return False
  counter()
  return True


'''
Recursively traverse directories to get files
'''
def recursive_traversal(rootdir):
  global global_keysfound
  global keywords
  global counter
  counter = initCounter(0)

  print "recursivetraversal ", rootdir

  for path, dirs, files in os.walk(rootdir):
      files = [os.path.join(path, f) for f in files]
      files = [f for f in files if not re.match(excludes, f)]
      files = [f for f in files if re.match(includes, f)]
      for filename in files:
         if isFileNameOkay(filename):
           search(os.path.join(path, filename))

  keywords_set = set(keywords)
  #global_keysfound = set(global_keysfound)
  print 'Looked in', counter(), 'files'
  print 'Used: ', prettyPrint(global_keysfound)
  print 'Not used: ', prettyPrint((keywords_set - global_keysfound))

def main(argv):
  root = rootdir
  try:
    opts, args = getopt.getopt(argv, "r:")
  except getopt.GetoptError:
    print 'usage: search.py -r <root>'
    sys.exit(2)

  for opt, arg in opts:
    if opt in ("-r"):
      root = arg
    else:
     print 'search.py -r <rootdir>'
     sys.exit(1)
  recursive_traversal(root)

if __name__ == "__main__":
  main(sys.argv[1:])

