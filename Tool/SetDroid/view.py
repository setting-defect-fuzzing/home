import logging
import os
import hashlib

class View(object):

    def __init__(self, line, father, sons):
        self.level=line.find('<node ')
        self.father=father
        self.line=line
        self.sons=sons
        self.instance = -1
        self.extract_attributes()

    def extract_attributes(self):
        self.index=self.get_attribute('index=')
        self.text=self.get_attribute('text=')
        self.resourceId=self.get_attribute('resource-id=')
        self.className=self.get_attribute('class=')
        self.package=self.get_attribute('package=')
        self.description=self.get_attribute('content-desc=')
        self.checkable=self.get_attribute('checkable=')
        self.clickable=self.get_attribute('clickable=')
        self.enabled=self.get_attribute('enabled=')
        self.focusable=self.get_attribute('focusable=')
        self.focused=self.get_attribute('focused=')
        self.scrollable=self.get_attribute('scrollable=')
        self.longClickable=self.get_attribute('long-clickable=')
        self.password=self.get_attribute('password=')
        self.selected=self.get_attribute('selected=')
        self.visibleToUser=self.get_attribute('visible-to-user=')
        self.bounds=self.get_attribute('bounds=')
        self.get_bounds_value()

    def get_attribute(self,keywords):
        line=self.line
        attributenum=line.find(keywords)
        line=line[attributenum+len(keywords)+1:len(line)-1]
        marksnum=line.find('\"')
        attribute=line[0:marksnum]
        # print(keywords+":"+attribute)
        return attribute
    
    def set_instance(self,instance):
        self.instance = instance

    def get_bounds_value(self):
        num1=self.bounds.find(",")
        self.xmin=self.bounds[1:num1]
        num2=self.bounds.find("]")
        self.ymin=self.bounds[num1+1:num2]
        
        line=self.bounds[num2+1:len(self.bounds)]

        num1=line.find(",")
        self.xmax=line[1:num1]
        num2=line.find("]")
        self.ymax=line[num1+1:num2]

        self.x = (int(self.xmin)+int(self.xmax)) /2
        self.y = (int(self.ymin)+int(self.ymax)) /2
    
    def add_son(self,son):
        self.sons.append(son)
    
    def print_tree(self):
        print("level_"+str(self.level)+":"+self.line)
        for son in self.sons:
            son.print_tree()
    
    def same(self,view):
        if self.line != view.line :
            return False
        for myson in self.sons:
            flag = False
            for hisson in view.sons:
                if myson.same(hisson):
                    flag=True
                    break
            if flag==False:
                return False
        return True
    
    def same_but_not_language(self,view):
        if self.resourceId != view.resourceId :
            return False
        for myson in self.sons:
            flag = False
            for hisson in view.sons:
                if myson.same_but_not_language(hisson):
                    flag=True
                    break
            if flag==False:
                return False
        return True
        


   