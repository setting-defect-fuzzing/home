import logging
import os
import hashlib
from view import View
"""
Record the information of the app's state
"""
class State(object):

    def __init__(self, lines):
        self.lines=lines
        self.classname_list = []
        self.resourceid_list = []
        self.num_list = []
        self.all_views=self.get_view()
        self.views=[]
        for view in self.all_views:
            if view.level == 2:
                self.views.append(view)
    
    def same_but_not_language(self,state):
        for view in self.views:
            if "com.google.android.inputmethod.latin" not in view.line and "com.android.systemui" not in view.line: #Decrease accuracy
                flag = False
                for view2 in state.views:
                    if view.same_but_not_language(view2):
                        flag=True
                        break
                if flag==False:
                    return False
        return True

    def same(self,state):
        for view in self.views:
            if "com.google.android.inputmethod.latin" not in view.line and "com.android.systemui" not in view.line: #Decrease accuracy
                flag = False
                for view2 in state.views:
                    if view.same(view2):
                        flag=True
                        break
                if flag==False:
                    return False
        return True

    def get_instance(self,view):
        #get_instance
        flag = False
        i=0
        while i < len(self.classname_list):
            if self.classname_list[i] == view.className and self.resourceid_list[i] == view.resourceId:
                flag = True
                self.num_list[i]=self.num_list[i]+1
                view.set_instance(self.num_list[i])
                break
            i=i+1
        if flag == False:
            self.classname_list.append(view.className)
            self.resourceid_list.append(view.resourceId)
            self.num_list.append(0)
            view.set_instance(0)
        return view

    def get_view(self):
        all_views=[]
        stack=[]
        for line in self.lines:
            if '<node ' in line and '/>' in line:
                if len(stack)==0:
                    view=View(line,None,[])
                else:
                    view=View(line,stack[len(stack)-1],[])
                    stack[len(stack)-1].add_son(view)
                view = self.get_instance(view)
                all_views.append(view)
            elif '<node ' in line:
                if len(stack)==0:
                    view=View(line,None,[])
                else:
                    view=View(line,stack[len(stack)-1],[])
                view = self.get_instance(view)
                stack.append(view)
            elif '</node>' in line:
                view=stack[len(stack)-1]
                stack.pop()
                view = self.get_instance(view)
                all_views.append(view)
                if len(stack)>0:
                    stack[len(stack)-1].add_son(view)
        
        return all_views

