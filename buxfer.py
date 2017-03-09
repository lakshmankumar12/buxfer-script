#!/usr/bin/python

import csv
import sys

tag_split = {}

def add_to_tag(tag_split,tag,amount,detail):
  f = float(amount.translate(None,'+,'))
  if tag not in tag_split:
    tag_split[tag] = [ 0.0 , [] ]
  tag_split[tag][0] += f
  detail.append(f)
  tag_split[tag][1].append(detail)

with open("transactions.csv","rb") as csfile:
  values = csv.reader(csfile)
  # skip first line always
  next(values)
  for transaction in values:
    try:
       #Date,Description,Currency,Amount,Type,Tags,Account,Status,Memo,Loans
       date,description,currency,amount,type,tag,account = transaction[:7]
    except ValueError as e:
        print "Got valueError in line:%s, err:%s"%(transaction, str(e))
        sys.exit(1)
    if type != "Expense":
      continue
    tag_elements = tag.split(',')
    if len(tag_elements) >= 2:
      # many tags
      for each_tag in tag_elements:
        try:
          tag_name,value = each_tag.split(":")
          add_to_tag(tag_split,tag_name,value,[date,description])
        except ValueError:
          print "%s has trouble in name,value -- %s"%(each_tag,transaction)
    else:
      add_to_tag(tag_split,tag,amount,[date,description])

sorted_tags = tag_split.keys()
sorted_tags.sort(key=lambda tag: tag_split[tag][0])

for i in sorted_tags:
  print "Tag: %s"%i
  items = tag_split[i][1]
  items.sort(key=lambda i: i[2])
  for j in tag_split[i][1]:
    print "  %-20s %15.2lf %s"%(j[0],j[2],j[1])

for i in sorted_tags:
  print "%-30s  %15.2lf"%(i,tag_split[i][0])

