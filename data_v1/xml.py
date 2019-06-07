#encoding:utf-8

import pickle
import link_analyzing

xml = open('resource.xml','a')

r =  open('result_array.pkl','rb')
p = pickle.load(r)


xml.write('<?xml version="1.0" ?>\n')

xml.write('<books>\n')

for i in p:
    xml.write('  <book>\n')
    xml.write('    <name>' + i['name'] + '</name>\n')
    xml.write('    <author>' + i['author'] + '</author>\n')
    xml.write('    <age>' + i['age'] + '</age>\n')
    xml.write('    <link>' +  link_analyzing.analyze_link(i) + '</link>\n')
    xml.write('  </book>\n')
xml.write('</books>\n')
