#!/usr/bin/env python

import os.path as p
from bs4 import BeautifulSoup

DIR_OF_THIS_SCRIPT = p.dirname( p.abspath( __file__ ) )
PATH_TO_DEMO_SCRIPT = p.join( DIR_OF_THIS_SCRIPT, '../demo.html' )

def getDocument( content ):
  return BeautifulSoup( content, 'html5lib', from_encoding = 'utf-8' )


def recursiveInline( path, already_inlined, final_doc ):
  path = p.abspath( path )
  if path in already_inlined:
    return
  already_inlined.add( path )
  content = open( path ).read()
  doc = getDocument( content )
  while True:
    links = doc.select( 'link[rel="import"]' )
    if not links:
      break
    link = links[ 0 ]
    new_path = p.join( p.dirname( path ), link[ 'href' ] )
    link.decompose()
    recursiveInline( new_path, already_inlined, final_doc )

  for child in doc.body.children:
    if child.name != 'stat-block':
      final_doc.body.append( child )
  for child in doc.head.children:
    if str( child ).strip():
      final_doc.head.append( child )


def finalDoc():
  already_inlined = set()
  doc = getDocument( '' )
  recursiveInline( PATH_TO_DEMO_SCRIPT, already_inlined, doc )
  new_doc = getDocument( open( PATH_TO_DEMO_SCRIPT ).read() )
  doc.body.append( new_doc.find( 'stat-block') )
  return doc


def main():
  print '<!DOCTYPE html>'
  print finalDoc()


if __name__ == "__main__":
  main()
