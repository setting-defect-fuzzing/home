import random
from event import Event
from view import View

"""
The policy of exploration
"""
class Policy(object):

    def __init__(self,devices,app,emulator_path,android_system,root_path):
        
        self.app = app
        self.devices = devices
        self.emulator_path = emulator_path
        self.android_system = android_system
        self.root_path = root_path
    
    def choice_event(self):
        pass

class RandomPolicy(Policy):
    def __init__(self,devices,app,emulator_path,android_system,root_path,
                pro_click,pro_longclick,pro_scroll,pro_edit,pro_naturalscreen,pro_leftscreen,pro_back,pro_splitscreen,pro_home):
        
        self.pro_click = pro_click
        self.pro_longclick = pro_click+pro_longclick
        self.pro_scroll = pro_click+pro_longclick+pro_scroll
        self.pro_edit = pro_click+pro_longclick+pro_scroll+pro_edit
        self.pro_naturalscreen = pro_click+pro_longclick+pro_scroll+pro_edit+pro_naturalscreen
        self.pro_leftscreen = pro_click+pro_longclick+pro_scroll+pro_edit+pro_naturalscreen+pro_leftscreen
        self.pro_back = pro_click+pro_longclick+pro_scroll+pro_edit+pro_naturalscreen+pro_leftscreen+pro_back
        self.pro_splitscreen = pro_click+pro_longclick+pro_scroll+pro_edit+pro_naturalscreen+pro_leftscreen+pro_back+pro_splitscreen
        self.pro_home = pro_click+pro_longclick+pro_scroll+pro_edit+pro_naturalscreen+pro_leftscreen+pro_back+pro_splitscreen+pro_home
        self.app = app
        self.devices = devices
        self.emulator_path = emulator_path
        self.android_system = android_system
        self.root_path = root_path
        self.pro_all=pro_click+pro_longclick+pro_scroll+pro_edit+pro_naturalscreen+pro_leftscreen+pro_back+pro_splitscreen+pro_home

    def random_text(self):
        text_style=random.randint(0,8)
        text_length=random.randint(1,5)
        nums=["0","1","2","3","4","5","6","7","8","9"]
        letters=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        symbols=[",",".","!","?"]
        i=0
        random_string=""
        if text_style == 0:
            while i < text_length:
                now_num=nums[random.randint(0,len(nums)-1)]
                random_string=random_string+now_num
                i=i+1
        elif text_style == 1:
            while i < text_length:
                now_letters=letters[random.randint(0,len(nums)-1)]
                random_string=random_string+now_letters
                i=i+1
        elif text_style == 2:
            while i < text_length:
                s_style=random.randint(0,2)
                if s_style==0:
                    now_letters=nums[random.randint(0,len(nums)-1)]
                    random_string=random_string+now_letters
                elif s_style==1:
                    now_letters=letters[random.randint(0,len(letters)-1)]
                    random_string=random_string+now_letters
                elif s_style==2:
                    now_letters=symbols[random.randint(0,len(symbols)-1)]
                    random_string=random_string+now_letters
                i=i+1
        elif text_style == 3:
            country=["Beijing","London","Paris","New York","Tokyo"]
            countrynum=random.randint(0,4)
            random_string=country[countrynum]
        elif text_style ==4:
            random_string=letters[random.randint(0,len(letters)-1)]
        elif text_style ==5:
            random_string=nums[random.randint(0,len(nums)-1)]
        elif text_style ==6:
            special_text=["www.google.com","t"]
            specialnum=random.randint(0,len(special_text)-1)
            random_string=special_text[specialnum]
        return random_string
    
    def choice_event(self,device,event_count):
        event_type = random.randint(0,self.pro_all-1)
        event=None
        click_classname_lists=["android.widget.RadioButton","android.view.View","android.widget.ImageView","android.widget.View","android.widget.CheckBox","android.widget.Button","android.widget.Switch","android.widget.ImageButton","android.widget.TextView","android.widget.CheckedTextView","android.widget.TableRow","android.widget.EditText","android.support.v7.widget.ar"]
        click_classname_lists_important=["android.widget.CheckBox","android.widget.Button","android.widget.Switch"]
        click_package_lists=[self.app.package_name,"android","com.android.settings","com.google.android",
        "com.google.android.inputmethod.latin","com.google.android.permissioncontroller","com.android.packageinstaller","com.android.permissioncontroller","com.google.android.packageinstaller"]
        print("random:"+str(event_type))
        if event_type<self.pro_click:
            views=[]
            import_views=[]
            for view in device.state.all_views:
                if view.className in click_classname_lists_important and view.package in click_package_lists :
                    views.append(view)
                    import_views.append(view)
                if view.className in click_classname_lists and view.package in click_package_lists :
                    views.append(view)
            if len(views)>0:
                event_view_num = random.randint(0,len(views)-1)
                event_view = views[event_view_num]
                event = Event(event_view, "click", device,event_count)  
            else:
                # print("re_choice")
                event = self.choice_event(device,event_count)
        elif event_type<self.pro_longclick:
            # print("longclick")
            if device.use(longClickable=True).count<1:
                # print("re_choice")
                event = self.choice_event(device,event_count)
            else:
                views=[]
                for view in device.state.all_views:
                    if view.className in click_classname_lists and view.package in click_package_lists and (view.longClickable=="true" or view.clickable=="true"):
                        views.append(view)
                if len(views)>0:
                    event_view_num = random.randint(0,len(views)-1)
                    event_view = views[event_view_num]
                    event = Event(event_view, "longclick", device,event_count)
                else:
                    # print("re_choice")
                    event = self.choice_event(device,event_count)
        elif event_type<self.pro_scroll:
            # print("scroll")
            if device.use(scrollable=True).count<1:
                # print("re_choice")
                event = self.choice_event(device,event_count)
            else:
                views=[]
                for view in device.state.all_views:
                    if view.scrollable=="true":
                        views.append(view)
                if len(views)>0:
                    event_view_num = random.randint(0,len(views)-1)
                    event_view = views[event_view_num]
                    direction_list = ["backward","forward","right","left"]
                    direction_num = random.randint(0,len(direction_list)-1)
                    event = Event(event_view, "scroll_"+direction_list[direction_num], device,event_count)
                else:
                    # print("re_choice")
                    event = self.choice_event(device,event_count)
        elif event_type<self.pro_edit:
            if device.use(className="android.widget.EditText").count<1:
                # print("re_choice")
                event = self.choice_event(device,event_count)
            else:
                views=[]
                for view in device.state.all_views:
                    if view.className == "android.widget.EditText":
                        views.append(view)
                if len(views)>0:
                    event_view_num = random.randint(0,len(views)-1)
                    event_view = views[event_view_num]
                    event = Event(event_view, "edit", device,event_count)
                    text = self.random_text()
                    event.set_text(text)
                else:
                    # print("re_choice")
                    event = self.choice_event(device,event_count)
        elif event_type<self.pro_naturalscreen:
            # print("naturalscreen")
            if device.use.orientation == "left":
                event = Event(None, "naturalscreen", device,event_count)
            else:
                event = self.choice_event(device,event_count)
        elif event_type<self.pro_leftscreen:
            # print("leftscreen")
            if device.use.orientation == "natural":
                event = Event(None, "leftscreen", device,event_count)
            else:
                event = self.choice_event(device,event_count)
        elif event_type<self.pro_back:
            # print("back")
            if self.app.main_activity != device.use.app_current()['activity']:
                event = Event(None, "back", device,event_count)
            else:
                event = self.choice_event(device,event_count)
        elif event_type<self.pro_splitscreen:
            # print("splitscreen")
            event = Event(None, "splitscreen", device,event_count)
        else:
            # print("home")
            event = Event(None, "home", device,event_count)
        return event
        

