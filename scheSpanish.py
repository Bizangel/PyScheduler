import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import colorchooser
from os import getcwd
import requests

def beauty_string(string):
    '''Receives a string and makes that every first letter of a word is caps and all other are lower, returns new string '''
    wordlist = string.split(' ')
    remaked = []
    for word in wordlist:
        if len(word) > 1: remaked.append( word[0].upper() + word[1:].lower() )
        else: remaked.append( word.upper() )
        

    return (' '.join(remaked))

def get_path():
    '''Returns current path in / instead of \ window stuff'''
    path = getcwd()
    path = path.replace('\\','/')
    return path

def difference_check(classdict,save_state):
    ''' receives save_state and current classdict, checks if there has been any difference on current schedule or not '''
    alist = []
    for key in classdict.keys():
        alist.append (classdict[key].request_save() )
    return str(alist) != save_state.get()

def get_current_save_state(classdict):
    '''returns current savestate as a list string '''
    alist = []
    for key in classdict.keys():
        alist.append (classdict[key].request_save() )
    return str(alist)

def hextorgb(hexstring):
    '''receives a hexstring and returns equivalent rgb tuple '''
    rstring = hexstring[1:3]
    gstring = hexstring[3:5]
    bstring = hexstring[5:7]
    return (int(rstring,16),int(gstring,16),int(bstring,16))

def save_config(show_title,timestamp_show,schedulepath):
    '''Saves current state in config.cfg '''
    config = open('config.cfg','w')
    config.write('global lastfile,pre_title_show,pre_timestamp_show\n')
    config.write('lastfile = \''+schedulepath.get()+'\'\n')
    config.write('pre_title_show = ')
    if show_title.get(): config.write('True\n')
    else: config.write('False\n')
    config.write('pre_timestamp_show = ')
    if timestamp_show.get(): config.write('True')
    else: config.write('False')
    config.close()
def b_or_w(rgb):
    '''receives a rgb tuple and returns the hex value of black of white according to the color, so it looks nicely. '''
    red,green,blue = rgb
    if (red*0.299 + green*0.587 + blue*0.114) > 186:
        return '#000000'
    else:
        return '#ffffff'

def on_exit(root,show_title,show_timestamp,schedulepath,unsaved,invoke_save):
    '''run whenever X is clicked on corner by user '''
    save_config(show_title,show_timestamp,schedulepath)
    if unsaved.get():
        answer = asksave()
        if answer == 0:
            return
        elif answer == 1:
            root.destroy()
        elif answer == 2:
            #save and destroy
            invoke_save.invoke() #saves
            root.destroy()
            
    else: #has saved just simply closed
        root.destroy()
    
def update_title_show(show_title,title_label):
    show = show_title.get()
    if show:
        title_label['fg'] = 'black'
    else:
        title_label['fg'] = '#f0f0f0'

def update_timestamp_show(show_timestamp,classdict):
    show = show_timestamp.get()
    for key in classdict.keys():
        classdict[key].show_timestamp(show)

def new_file(canvas,classdict,unsaved,invoke_save,schedulepath,filename):
    if unsaved.get():
        answer = asksave()
        if answer == 0: return 
        elif answer == 1: pass #don't save
        elif answer == 2: invoke_save.invoke()

    initpath = get_path()
    initpath += '/schedules'
    filepath=  filedialog.asksaveasfilename(initialdir = initpath,title = "Nuevo Horario...",filetypes = (("Archivos de Horario","*.txt"),("Todos","*.*")),
                                            initialfile='nuevo_horario',defaultextension='*.txt')
    if filepath == '': return 
    #gets path
    filename.set(filepath)
    schedulepath.set(filepath)
    #sets path
    keys = list(classdict.keys())
    
    for key in keys:
        classdict[key].delete(canvas,classdict,noask=True) #deletes all classes

    invoke_save.invoke() #saves on new file

def ask_for_new_path():
    '''asks the user for new path and returns it '''
    initpath = get_path()
    initpath += '/schedules'
    filepath=  filedialog.asksaveasfilename(initialdir = initpath,title = "Nuevo Horario...",filetypes = (("Archivos de Horario","*.txt"),("Todos","*.*")),
                                            initialfile='nuevo_horario',defaultextension='*.txt')
    return filepath
def open_file(canvas,classdict,reference_channel,unsaved,invoke_save,schedulepath,filename):
    '''Asks for the user for path and open schedules '''
    if unsaved.get():
        answer = asksave()
        if answer == 0: return
        elif answer == 1: pass #continue and don't save
        elif answer == 2: invoke_save.invoke() #saves
            
            
        
    initpath = get_path() #gets folder path
    initpath += '/shedules'
    path = filedialog.askopenfilename(initialdir =initpath,title = "Escoger Archivo...",filetypes = (("Archivos de Horario","*.txt"),("Todos","*.*")))
    if path == '': return #Do nothing if no path given

    temp = path.split('/')
    temp = temp[-1]
    temp = temp.strip('.txt')
    filename.set(temp)
    
    schedulepath.set(path) #sets path
    keys = list(classdict.keys())
    
    for key in keys:
        classdict[key].delete(canvas,classdict,noask=True) #deletes all classes
    open_schedule(path,canvas,classdict,reference_channel) #remakes
    invoke_save.invoke() #saves new schedule
    
def open_schedule(path,canvas,classdict,reference_channel):
    '''Tries to open a schedule'''
    try:
        info = open(path,'r').read()
        exec(info)
    except:
        error_popup('No se pudo abrir el archivo')
        return
    
    for subjectinfo in readlist: #
        decrypt_save_readlist(subjectinfo,canvas,classdict,reference_channel)

def save_file(classdict,pathvar,save_state,invokebutton):
    '''Receives classdict to save file and a already defined path, to save directly '''
    path = pathvar.get()
    alist = []
    for key in classdict.keys():
        alist.append (classdict[key].request_save() )
    filetosave = open(path,'w')
    filetosave.write('global readlist\n'+'readlist = '+str(alist))
    filetosave.close()
    #updates savestate
    save_state.set( get_current_save_state(classdict) )

    invokebutton.invoke() #update title
    
def save_as_file(classdict,save_state,invokebutton,filename,schedulepath):
    '''Receives classdict, and asks the user where to save '''
    alist = []
    for key in classdict.keys():
        alist.append (classdict[key].request_save() )
    
    initpath = getcwd() #gets folder path
    initpath += '\\schedules'
    filepath=  filedialog.asksaveasfilename(initialdir = initpath,title = "Guardar Como...",filetypes = (("Archivos de Horario","*.txt"),("Todos","*.*")),
                                            initialfile=filename.get(),defaultextension='*.txt')
    if filepath == '': return #Do nothing if no path given
    filetosave = open(filepath,'w')
    filetosave.write('global readlist\n'+'readlist = '+str(alist))
    filetosave.close()
    save_state.set( get_current_save_state(classdict) ) #updates savestate

    schedulepath.set(filepath)

    temp = filepath.split('/')
    temp = temp[-1]
    temp = temp.strip('.txt')
    filename.set(temp)

    
    invokebutton.invoke() #update title
    
def read_class_info(classinfo):
    '''Receives a classinfo style list and transform the daystrings into their proper day ID, returns a new list and does not modify old '''
    returnlist = []
    for info in classinfo:
        daystring,start,stop = info
        dayid = daystring_index(daystring)
        returnlist.append( (dayid,start,stop) )
    return returnlist

def daystring_index(daystring):
    '''Receives a daystring of spanish/english initials or full value namesand returns the day id from 0 to 6 '''
    daystring = daystring.upper()
    if daystring == 'LU' or daystring == 'MON': return 0
    elif daystring == 'MA' or daystring == 'TUE': return 1
    elif daystring == 'MI' or daystring == 'WED': return 2
    elif daystring == 'JU' or daystring == 'THU': return 3
    elif daystring == 'VI' or daystring == 'FRI': return 4
    elif daystring == 'SA' or daystring == 'SAT': return 5
    elif daystring == 'DO' or daystring == 'SUN': return 6

    #full names
    daystring = daystring.lower()
    if daystring == 'lunes' or daystring == 'monday': return 0
    elif daystring == 'martes' or daystring == 'tuesday': return 1
    elif daystring == 'miercoles' or daystring == 'wednesday' or daystring == 'miércoles': return 2
    elif daystring == 'jueves' or daystring == 'thursday': return 3
    elif daystring == 'viernes' or daystring == 'friday': return 4
    elif daystring == 'sabado' or daystring == 'saturday' or daystring == 'sábado': return 5
    elif daystring == 'domingo' or daystring == 'sunday': return 6
    else:
        raise(ValueError('No appropiate day string given.'))
def index_to_daystring(dayindex):
    '''Receives a day index and returns the corresponding string in ENGLISH '''
    if dayindex == 0: return 'Monday'
    elif dayindex == 1: return 'Tuesday'
    elif dayindex == 2: return 'Wednesday'
    elif dayindex == 3: return 'Thursday'
    elif dayindex == 4: return 'Friday'
    elif dayindex == 5: return 'Saturday'
    elif dayindex == 6: return 'Sunday'

def process_title_save(root,classdict,save_state,filepath,unsaved):
    '''Process the save difference and updates title accordingly '''
    titlelabel = ''
    difference = difference_check(classdict,save_state)
    if difference: titlelabel += '*'
    titlelabel += 'PyScheduler ' + filepath.get()
    if difference: titlelabel += '*'
    root.title(titlelabel)

    if difference:
        unsaved.set(1)
    else: unsaved.set(0)
    
def remove_empty(alist,string=False):
    '''Removes all empty strings in a list OR all empty characters in a string'''
    if string:
        temp = ''
        for let in alist:
            if let != ' ': temp += let
        return temp
    else:
        while '' in alist:
            alist.remove('')
def floathour_to_string(floathour):
    '''Receives a floathour and returns the corresponding string in AM PM format '''
    minutes = (floathour % 1) * 60
    hour = floathour // 1
    if hour == 24: return '12:00AM'
    if hour > 12:
        hour -= 12
        ampm = 'PM'
    elif hour == 12:
        ampm = 'PM'
    elif hour < 12:
        ampm ='AM'
    if hour == 0: hour = 12
    
    minutes = int(minutes)
    hour = int(hour)
    if minutes != 0: return str(hour)+':'+str(minutes)+ampm
    else: return str(hour) + ':' + '00' + ampm #ensure double 00

def read_day(daystring):
    '''Receives the string within parentheses and reads it'''
    if daystring[0] == '(' and daystring[-1] == ')':
        splitted = daystring.split(',')
        return day,interval
    else:
        return

def canvasRect(canvas,topleft,width,height,color='red'):
    '''Receives a canvas width and height and topleft point to create rect on canvas, returns the poly for later deletion '''
    left = topleft[0]
    top = topleft[1]
    poly = canvas.create_polygon(topleft,(left+width,top),(left+width,top+height),(left,top+height),fill=color)
    return poly

#the classdict points to a OBJECT of the SUBJECT class that contains the SQUARES so that delete calls SUBJECT delete and deletes all containing squares
class classSquare:
    def __init__(self,canvas,classdict,dayid,start,end,title,reference_channel,color='red'):
        height = (end-start)*45

        contrastcolor = b_or_w(hextorgb(color))
        self.title = title
        self.teacher = ''
        
        #self.killbutton = tk.Button(canvas,text='X',fg='red',bg='gray',command=lambda:classdict[self.title].delete(canvas,classdict)) -- deprecated killbutton
        #self.killbutton.place(x=80+120*dayid+95,y=(start-6)*45+height-13,relwidth=0.02,relheight=0.02)
        
        if end-start > 1.5: fontsize,optjump = 13,'\n'
        else: fontsize,optjump = 10,''
        
        textlabel = title
        textlabel += '\n'
        self.original_textlabel = textlabel
        self.timestamp =  floathour_to_string(start) + '-' + optjump + floathour_to_string(end) 
        textlabel += self.timestamp #add timestamp on creation by default
        

        

        
        self.label = tk.Label(canvas,text=textlabel,bg=color,wraplength=110,fg=contrastcolor,font=('ComicSans',fontsize))
        self.label.bind('<Button-3>',self.popup)

        self.popup_menu = tk.Menu(self.label, tearoff=0)
        self.popup_menu.add_command(label="Editar",
                                    command=lambda: self.open_edit_window(canvas,classdict,reference_channel,title) )
        self.popup_menu.add_command(label="Añadir/Editar Profesor",
                                    command=lambda: self.open_teacher_window(canvas,classdict,reference_channel,title) )
        self.popup_menu.add_command(label="Eliminar",
                                    command=lambda: classdict[self.title].delete(canvas,classdict))
        #self.popup_menu.add_command(label="Select All",
        #                            command=self.select_all)
        
        #self.rect = canvasRect(canvas,(80+110*dayid, (start-6)*45 ),110,height,color)
        
        self.label.place(x=80+110*dayid,y=(start-6)*45,width=110,height=height)
        

        self.infostring = index_to_daystring(dayid) + ': ' + floathour_to_string(start) + '-' + floathour_to_string(end)
        self.show_timestamp = True
    def delete(self,canvas,classdict):
        '''Receives canvas and deletes self from canvas, classdict is done outside from subject class '''
        #canvas.delete(self.rect)
        self.label.place_forget()
        #self.killbutton.place_forget() --- killbutton deprecated

    def get_string(self):
        ''' Gets the string info of the class square in the the <day>: <start time>-<end time> format'''
        return self.infostring

    def popup(self,event):
        try:
            self.popup_menu.tk_popup(event.x_root+70, event.y_root+20, 0)
        finally:
            self.popup_menu.grab_release()
    def open_edit_window(self,canvas,classdict,reference_channel,title):
        ID = reference_channel[0]
        ID += 1
        reference_channel[0] = ID
        EditWindow(canvas,classdict,reference_channel,title)

    def open_teacher_window(self,canvas,classdict,reference_channel,title):
        reference_channel[0] +=1
        TeacherPopUp(canvas,classdict,title)
        
        
    def update_display_label(self):
        textlabel = self.original_textlabel
        if self.show_timestamp: textlabel += self.timestamp + '\n'
        textlabel += self.teacher
        self.label['text'] = textlabel
        if len(textlabel) > 80: self.label['font'] = ('ComicSans',7)
        elif len(textlabel) > 50: self.label['font'] = ('ComicSans',8)
        elif len(textlabel) > 30: self.label['font'] = ('ComicSans',10)
        else: self.label['font'] = ('ComicSans',13)
    
        
class Subject: #class info format is a list of tuple trios containing (<day>,<start>,<end>) ex: [(2,9,11),(4,9,11)]  this means class on WED and FRI from 9-11
    def __init__(self,canvas,classdict,title,classinfo,reference_channel,n_credits,color='red'):
        self.reference_channel = reference_channel
        self.n_credits = n_credits #as an int already
        self.squares = [] #list that holds class squares
        self.title = title
        for info in classinfo: #create classsquares
            dayid,start,end = info
            self.squares.append( classSquare(canvas,classdict,dayid,start,end,title,reference_channel,color )   )
        
        classdict[title] = self #self reference will be as identifier in classdict
        self.color = color
    def delete(self,canvas,classdict,noask=False):
        '''Deletes all classes in current subject'''
        if noask:
            for square in self.squares: #deletes all square objects
                square.delete(canvas,classdict)
            del classdict[self.title] #deletes class entry from dictionary

            temp = self.reference_channel[1].get()
            temp -= self.n_credits
            self.reference_channel[1].set(temp)
            self.reference_channel[3].invoke() #update title
            return
        #else keep going
        if messagebox.askokcancel("Eliminar", "¿Seguro que quieres eliminar {0}?".format(self.title)):
            for square in self.squares: #deletes all square objects
                square.delete(canvas,classdict)
            del classdict[self.title] #deletes class entry from dictionary
            temp = self.reference_channel[1].get()
            temp -= self.n_credits
            self.reference_channel[1].set(temp)
            self.reference_channel[3].invoke() #update title

    def parse_class_info(self):
        '''Returns a list of strings including the class info of each square in the <day>: <start time>-<end time> format '''
        returnlist = []
        for squareclass in self.squares:
            returnlist.append(squareclass.get_string())
        return returnlist

    def request_save(self):
        '''Returns list of strings classinfo with the identifier as the first element and the color as second and teacher string as third n_credits as fourth and
        rest are blockstrings.'''
        returnlist = [self.title,self.color,self.get_teacher(),self.n_credits]
        returnlist.extend(self.parse_class_info())
        return returnlist

    def set_teacher(self,teacherstring):
        '''Sets teacher name for all class blocks '''
        for square in self.squares:
            square.teacher = teacherstring
            square.update_display_label() #update display label
        if self.reference_channel[3] != 1:self.reference_channel[3].invoke() #update title 

    def get_teacher(self):
        '''Returns current subject teacher name '''
        return self.squares[0].teacher

    def show_timestamp(self,show_timestamp):
        '''Receives a bool of show_timestamp and updates proper class squares to display or not timestamps '''
        for classblock in self.squares:
            classblock.show_timestamp = show_timestamp
            classblock.update_display_label()

    
            
        

def hrto24format(hourstring):
    '''Receives a hourstring that has number followed by :AM or :PM, transforms it into a 24hrs FLOAT where for example 8:30AM means 8.5 '''
    if len(hourstring) == 6:short = True #short means only 1 digit on start before : like 8:00AM
    else: short = False #not short more than 1, like 12:00AM
    
    time = 0
    ampm = hourstring[-2:]
    if ampm.upper() == 'PM':
        if short: time = int(hourstring[0])+12
        else:
            if hourstring[0:2] == '12': time = 12
            else:time = int(hourstring[0:2])+12
    else:
        if short: time = int(hourstring[0])
        else:time = int(hourstring[0:2])

    if short: time += int(hourstring[2:4])/60
    else: time += int(hourstring[3:5])/60

    return time
    
def decrypt_save_readlist(readlist,canvas,classdict,reference_channel):
    '''Receives a save readlist, decrypts it and creates the class '''
    title = readlist[0]
    classblocks = readlist[4:]
    classinfo = []
    for block in classblocks:
        classinfo.append(decrypt_classinfo(block) )
        
    createClass( canvas,classdict,title,classinfo,reference_channel,readlist[3],readlist[1] ) 
    #set teacher
    classdict[title].set_teacher(readlist[2])
def createClass(canvas,classdict,title,classinfo,reference_channel,n_credits,color='red'): #check subject constructor for classinfo parameters and style
    '''Receives all the necessary parameters to start a class, days are given by initials on english MON TUE WED THU FRI SAT or
    by TWO initials no spanish LU MA MI JU VI SA'''
    if title in classdict.keys():
        error_popup('Una Materia con ese nombre ya existe')
        return #ignore if already exists
    classinfo = read_class_info(classinfo) #transform daystrings to dayIDs
    #we apply daystring index on all first elements of classinfo
    Subject(canvas,classdict,title,classinfo,reference_channel,n_credits,color)
    #Add to credit numbers
    temp = reference_channel[1].get()
    temp += n_credits
    reference_channel[1].set(temp)
    #update label displays of subjects
    update_timestamp_show(reference_channel[2],classdict)
    if reference_channel[3] == 1:
        return
    #else invoke
    reference_channel[3].invoke() #call button update title method
    
def error_popup(errorstring):
    '''Receives a string and displays it as an error '''
    tk.messagebox.showerror('Error',errorstring)
def get_color(stringvar,label=None):
    '''Receives a string var and asks the user for color, saves the hex string in the given stringvar
    also an optional label to update the label color'''
    color = colorchooser.askcolor()
    if color == (None,None):
        return #do nothing
    hexcolor = color[1]
    stringvar.set(hexcolor)
    if label != None:
        label['bg'] = hexcolor
def setampm(ampm,ampm_string):
        '''Receives an ampm spinbox and a AM or PM string and sets the spinbox to that value'''
        if ampm_string == 'PM': ampm['values'] = ('PM','AM')
        else: ampm['values'] = ('AM','PM')

def check_overlap(time1,time2):
    '''Receives a time1 and time2 that are tuples that contains starthour and endhour in float 24hrs formats ex:(8.5,10)
    returns True if there is overlapping between the two timestamps '''
    x1,x2 = time1
    y1,y2 = time2
    return x2 > y1 and y2 > x1

def insert_string(string,index,substring):
    '''Receives a string a substring and an index, returns new string with
    substring indexed in'''
    returnstring = ''
    for i in range(len(string)):
        if i == index: returnstring += substring
        returnstring += string[i]
    return returnstring

def overlap_test(checkstring,classinfolist):
    '''Receives a classinfo string to check and returns if overlaps occurs '''
    checkinfo = decrypt_classinfo(checkstring)
    checkday = daystring_index(checkinfo[0])
    time1 = (checkinfo[1],checkinfo[2])
    for classinfo in classinfolist:
        info = decrypt_classinfo(classinfo)
        infoday = daystring_index(info[0])
        time2 = (info[1],info[2])
        if checkday == infoday and check_overlap(time1,time2):
            return True
            
                
    return False
  
def decrypt_classinfo(classinfo):
    '''Receives a classinfo string object that describes schedule times, returns tuple with (<daystring>,<start floathour>,<end floathour>)'''
    classinfo = classinfo.split(' ')
    classinfo[0] = classinfo[0].strip(':')
    daystring = classinfo[0]
    starthour,endhour = classinfo[1].split('-')
    starthour = hrto24format(starthour)
    endhour = hrto24format(endhour)
    return (daystring,starthour,endhour)
   
class scheduleWindow:
    def __init__(self,canvas,classdict,reference_channel):
        self.toplevelid = reference_channel[0]
        self.classdict = classdict
        self.reference_channel = reference_channel
        self.pre_existant = []
        for key in classdict.keys():
            self.pre_existant.extend(  classdict[key].parse_class_info()   )
        #print (self.pre_existant)
        self.class_blocks = [] #keeps class blocks info strings
        self.canvas = canvas
        self.window = tk.Toplevel(canvas,takefocus=True)
        self.window.grab_set()
        self.window.title('Nueva Materia')
        self.window.geometry('300x300+900+300')
        self.window.resizable(False,False)

        self.entrytitle = tk.Entry(self.window)
        self.entrytitle.place(relx=0.18,rely=0.03)

        
        self.startminutes = tk.Spinbox(self.window,values=('00','15','30','45'),state='readonly',wrap=True)
        self.startminutes.place(relx=0.4,rely=0.3,relwidth=0.1)
        
        self.starthour = tk.Entry(self.window, validate="key",justify='right',bg='#f0f0f0')
        self.starthour['validatecommand'] = (self.starthour.register(self.inthourcheck),'%P','%d','%W')
        self.starthour.place(relx=0.25,rely=0.3,relwidth=0.1)
        
        self.endminutes = tk.Spinbox(self.window,values=('00','15','30','45'),state='readonly',wrap=True)
        self.endminutes.place(relx=0.4,rely=0.5,relwidth=0.1)
        
        self.endhour = tk.Entry(self.window, validate="key",justify='right',bg='#f0f0f0')
        self.endhour['validatecommand'] = (self.starthour.register(self.inthourcheck),'%P','%d','%W')
        self.endhour.place(relx=0.25,rely=0.5,relwidth=0.1)

        self.entrycredits = tk.Entry(self.window, validate='key', justify= 'right',bg='#f0f0f0')
        self.entrycredits['validatecommand'] = (self.entrycredits.register(self.intcreditscheck),'%P','%d')
        self.entrycredits.place(anchor='sw',relx=0.2,rely=1,relwidth=0.1)

        
        # --- /// --- /// --- Color Picker
        self.color = tk.StringVar()
        self.color.set('#ff0000')
        self.colorButton = tk.Button(self.window,text='Cambiar Color',command=lambda:get_color(self.color,self.colordisplay))
        self.colorButton.place(relx=1,rely=0.06,anchor='e')
        self.colordisplay = tk.Label(self.window,bg=self.color.get(),relief='raised')
        self.colordisplay.place(relx=0.62,rely=0.025,relwidth=0.07,relheight=0.07)

        
        self.start_ampm = tk.Spinbox(self.window,values=('AM','PM'),state='readonly',wrap=True,name='aname')
        self.start_ampm.place(relx=0.5,rely=0.3,relwidth=0.15)
        

        self.end_ampm = tk.Spinbox(self.window,values=('AM','PM'),state='readonly',wrap=True)
        self.end_ampm.place(relx=0.5,rely=0.5,relwidth=0.15)

        self.addblock_button = tk.Button(self.window,text='Agregar Bloque',command=lambda:self.add_class_block())
        self.addblock_button.place(relx=0.70,rely=0.15)

        self.weekday = tk.Listbox(self.window)
        self.weekday.insert(1,'Lunes')
        self.weekday.insert(2,'Martes')
        self.weekday.insert(3,'Miércoles')
        self.weekday.insert(4,'Jueves')
        self.weekday.insert(5,'Viernes')
        self.weekday.insert(6,'Sábado')
        self.weekday.place(relx=0.7,rely=0.275,relheight=0.35,relwidth=0.3)


        self.displaylabel = tk.Label(self.window,bg='lightgray')
        self.displaylabel.place(relx=0.1,rely=0.65,relwidth= 0.8,relheight = 0.25)
        self.displaylabel.bind('<Button-3>',self.popup)

        self.createButton = tk.Button(self.window,text='Crear!',bg='lightgray',command= lambda:self.send_class_info() )
        self.createButton.place(rely=1,anchor='s',relx=0.5)

        #testbutton = tk.Button(self.window,text='press me',command=lambda: self.start_ampm.get() )
        #testbutton.place(relx=0.1,rely=0)
        
        # --- /// --- /// --- /// text labels for gui indication
        a = tk.Label(self.window,text='Nombre:',font=('ComicSans',10))
        a.place(relx = 0,rely=0.02)
        self.class_block_display = tk.Label(self.window,text='--- Añadir Bloques --- /// --- /// -',font=('ComicSans',12))
        self.class_block_display.place(relx = 0,rely=0.15)
        a = tk.Label(self.window,text='Hora Inicio',wraplength=60,font=('ComicSans',12))
        a.place(relx=0.07,rely=0.265)
        a = tk.Label(self.window,text='Hora \n Fin',wraplength=60,font=('ComicSans',12))
        a.place(relx=0.07,rely=0.465)
        a = tk.Label(self.window,text =':',font=('ComicSans',16))
        a.place(relx=0.35,rely=0.278)
        a = tk.Label(self.window,text =':',font=('ComicSans',16))
        a.place(relx=0.35,rely=0.478)
        a = tk.Label(self.window,text='Créditos: ',font=('ComicSans',11))
        a.place(rely=1,relx=0.02,anchor='sw')
        # --- /// --- /// --- Right click label menu
        self.popup_menu = tk.Menu(self.displaylabel, tearoff=0,title='Delete')
        self.popup_menu.add_command(label="Eliminar Bloques",state='disabled')
        self.popup_menu.add_separator()
    def delete_block(self,blockstring):
        
        index = self.class_blocks.index(blockstring)
        self.class_blocks.remove(blockstring)
        self.update_display_label()
        self.popup_menu.delete(index+2)
        
    def send_class_info(self):
        '''Sends class info to the canvas and ensures proper Subject/class creation '''
        if len(self.class_blocks) == 0:
            error_popup('Añade almenos un bloque de clase')
            return
        elif self.entrytitle.get() == '':
            error_popup('Escribe un nombre')
            return
        classinfo_list = []
        for block in self.class_blocks:
            classinfo_list.append(decrypt_classinfo(block))

        class_credits = self.entrycredits.get()
        if len(class_credits) == 0: class_credits = 0
        class_credits = int(class_credits)
        createClass(self.canvas,self.classdict,self.entrytitle.get(),classinfo_list,self.reference_channel,class_credits,self.color.get())
        self.window.destroy()
    def add_class_block(self):
        daystring = self.weekday.curselection()
        if len(daystring) == 0:
            messagebox.showwarning('Falta Información','Favor selecciona un día')
            return
        daystring = self.weekday.get(daystring[0])
        starthour = self.starthour.get()
        endhour = self.endhour.get()
        if len(starthour) == 0 or len(endhour) == 0:
            messagebox.showwarning('Falta Información','Favor especificar hora inicio e hora fin')
            return 

        start_ampm = self.start_ampm.get()
        end_ampm = self.end_ampm.get()
        if (int(starthour) < 7 and start_ampm == 'AM') or ( 12 > int(starthour) > 7 and start_ampm == 'PM')or (int(starthour) == 12 and start_ampm=='AM'):
            error_popup('No se soportan horas antes de 7AM o después de 7PM')
            return
        elif (int(endhour) < 7 and end_ampm == 'AM') or (12 > int(endhour) > 7 and end_ampm == 'PM') or (int(endhour) == 12 and end_ampm=='AM'):
            error_popup('No se soportan horas antes de 7AM o después de 7PM')
            return

        startminutes = self.startminutes.get()
        endminutes = self.endminutes.get()
        startstring = starthour + ':' + startminutes + start_ampm
        endstring = endhour + ':' + endminutes + end_ampm

        if hrto24format(startstring) >= hrto24format(endstring):
            error_popup('Hora Inicio no puede ser mayor o igual que hora fin')
            return

        blockstring = daystring +': '+ starthour + ':' + startminutes + start_ampm + '-' + endhour + ':' + endminutes + end_ampm
        #check for overlapping and give warning
        if overlap_test(blockstring,self.pre_existant) or overlap_test(blockstring,self.class_blocks):
            if messagebox.askokcancel("Cruce de Bloques", "Añadir este bloque hará que se cruze con otro \n ¿Continuar? "):
                pass #keep the code going
            else:
                return 
            
        if blockstring not in self.class_blocks:
            self.class_blocks.append(blockstring)
            self.update_display_label()
            #update popup menu
            self.popup_menu.add_command(label=blockstring,command=lambda: self.delete_block(blockstring) )
        else:
            error_popup('Un bloque de clase con esas horas ya existe')
        
    def inthourcheck(self,string,command,widgetname):
        if len(string) > 2: return False

       
        try:
            n = int(string)
            canvasstring1 = '.!canvas.!toplevel.!entry2'
            canvasstring2 = '.!canvas.!toplevel.!entry3'
            
            if self.toplevelid == 1: insertstring = ''
            else: insertstring = str(self.toplevelid)
            widgetcheck1 = insert_string(canvasstring1,18,insertstring)
            widgetcheck2 = insert_string(canvasstring2,18,insertstring)
            if widgetname == widgetcheck1: #means start_hour
                if n >=7 and n != 12: setampm(self.start_ampm,'AM')
                elif n < 7 or n==12: setampm(self.start_ampm,'PM')
            elif widgetname == widgetcheck2: #means end_hour
                if n >= 7 and n != 12: setampm(self.end_ampm,'AM')
                elif n < 7 or n==12: setampm(self.end_ampm,'PM')
        except:
            pass
        
        if command == '1':
            try:
                n = int(string)
                if n > 12: return False
                elif n==0: return False
                return True
            except:
                return False
        return True
    def intcreditscheck(self,string,command):
        
        if command == '1':
            if len(string) > 1: return False
            try:
                n = int(string)
                return True
            except:
                return False
        return True

    def update_display_label(self):
        '''Updates display label to match block classes '''
        string = ''
        for classinfo in self.class_blocks:
            string += classinfo
            string += '\n'
        self.displaylabel['text'] = string
    def popup(self,event):
        try:
            self.popup_menu.tk_popup(event.x_root+40, event.y_root+10, 0)
        finally:
            self.popup_menu.grab_release()

class EditWindow(scheduleWindow):
    def __init__(self,canvas,classdict,reference_channel,title):
        #idea is to unpack classinfo and delete when sending new
        self.title = title
        
        super(EditWindow,self).__init__(canvas,classdict,reference_channel)
        classinfo = classdict[title].request_save() #parse info
        self.entrytitle.insert(0,title)
        self.entrycredits.insert(0,classinfo[3])
        self.teacher = classdict[title].get_teacher()
        self.window.title('Editar Materia')
        self.color.set(classinfo[1])
        self.colordisplay['bg'] = self.color.get()
        self.class_blocks = classinfo[4:]   #0 is title 1 is color ,2 is teacher, 3 are credits so start from 4 and on
        self.class_block_display['text'] = '--- Editar Bloques --- /// --- /// -'

        #recreate pop-up menu
        self.popup_menu = tk.Menu(self.displaylabel, tearoff=0,title='Delete')
        self.popup_menu.add_command(label="Eliminar Bloques",state='disabled')
        self.popup_menu.add_separator()
        
        self.initial_popup_adds()
        #remove current class blocks from pre-existant
        for blockstring in self.class_blocks:
            self.pre_existant.remove(blockstring)
        self.update_display_label()
        self.createButton['text'] = 'Editar!'

        
    def initial_popup_adds(self):
        for blockstring in self.class_blocks:
            
            self.add_popup_menu_delete(blockstring)
    def add_popup_menu_delete(self,blockstring):
        self.popup_menu.add_command( label= blockstring, command= lambda: self.delete_block(blockstring) )
    def send_class_info(self):
        if len(self.class_blocks) == 0:
            error_popup('Añade almenos un bloque de clase')
            return
        elif self.entrytitle.get() == '':
            error_popup('Escribe un nombre')
            return
        #delete previous entry
        self.classdict[self.title].delete(self.canvas,self.classdict,noask=True)
        classinfo_list = []
        for block in self.class_blocks:
            classinfo_list.append(decrypt_classinfo(block))
            
        class_credits = self.entrycredits.get()
        if len(class_credits) == 0: class_credits = 0
        else: class_credits = int(class_credits)
        createClass(self.canvas,self.classdict,self.entrytitle.get(),classinfo_list,self.reference_channel,class_credits,self.color.get())
        self.classdict[self.entrytitle.get()].set_teacher(self.teacher) #sets saved teacher
        self.window.destroy()

class TeacherPopUp:
    def __init__(self,canvas,classdict,title):
        self.window = tk.Toplevel(canvas,takefocus=True)
        self.window.grab_set()
        prevteacher = classdict[title].get_teacher()
        if len(prevteacher) == 0:self.window.title('Añadir Profesor')
        else: self.window.title('Editar Profesor')
        
        self.window.geometry('250x70+900+300')
        self.window.resizable(False,False)

        self.entry = tk.Entry(self.window)
        self.entry.place(relx=0.5,rely=0,relwidth=0.8,relheight=0.5,anchor='n')
        self.entry.insert(0,prevteacher)
        self.button = tk.Button(self.window,text='Confirmar',command=lambda: self.return_teacher_name(classdict,title) )
        self.button.place(rely=1,anchor='s',relx=0.5)

        self.window.bind('<Return>',lambda event: self.button.invoke())

        

    def return_teacher_name(self,classdict,title):
        '''Returns the entrybox teacher name '''
        classdict[title].set_teacher( self.entry.get() )
        self.window.destroy()

def asksave():
    '''Ask the user the asksave prompt and returns the user answer'''
    answer = messagebox.askyesnocancel('Confirmar','Tienes cambios sin guardar, ¿Deseas guardar?')
    if answer == None: return 0
    elif answer: return 2
    elif not answer: return 1
    
'''
class SavePopup:
    def __init__(self,canvas,reference_channel):
        self.reference_channel = reference_channel
        self.window = tk.Toplevel(canvas,takefocus=True)
        self.window.geometry('350x100+300+300')
        self.window.grab_set()
        self.window.title('Confirmation')
        self.window.protocol('WM_DELETE_WINDOW',lambda: self.returnchannel(0) )
        reference_channel[0] +=1 #increase id

        self.save = tk.Button(self.window,text='Save',command= lambda: self.returnchannel(2) )
        self.dont = tk.Button(self.window,text='Don\'t Save',command= lambda: self.returnchannel(1) )
        self.cancel = tk.Button(self.window,text='Cancel',command= lambda: self.returnchannel(0) )
        self.save.place(relx=0.2,rely=1,anchor='s',relwidth=0.2)
        self.dont.place(relx=0.5,rely=1,anchor='s',relwidth=0.2)
        self.cancel.place(relx=0.8,rely=1,anchor='s',relwidth=0.2)
        
        self.window.bind("<FocusOut>", self.Alarm)
    def Alarm(self,event):
        self.window.focus_force()
        self.window.bell()
    def returnchannel(self,index):
        self.reference_channel[3] = index
        self.window.destroy()
'''
def hr24toampm(string):
    '''Receives a string of 24hr and turns it into am or pm format'''
    hour,minutes = string.split(':')
    hour = int(hour)

    if hour >= 12: ampm = 'PM'
    else: ampm = 'AM'

    if hour > 12: hour -=12
    return str(hour)+':'+ minutes + ampm


    
    
def get_class_data(code,groupid,stringvar=None):
    '''Receives a class code and a groupid return all the class data info in the following way, also receives optional stringvar to show updated progress
    (title,teacher,[list of classtrings]) '''
    stringvar.set('Fetching Class Name...')
    name = requests.get('https://urapprest.uranalytics.p.azurewebsites.net/api/asignaturaDetalle?codigo={0}&opcionDetalle=DetalleActividad'.format(code))
    stringvar.set('Fetching Class Credits...')
    c_credits = requests.get('https://urapprest.uranalytics.p.azurewebsites.net/api/asignaturaDetalle?codigo={0}&opcionDetalle=DetalleAsignatura'.format(code))
    stringvar.set('Fetching Class Groups...')
    group = requests.get('https://urapprest.uranalytics.p.azurewebsites.net/api/asignaturaDetalle?codigo={0}&opcionDetalle=DetalleGrupo&codActividad={0}'.format(code))             

    json_name = name.json()
    json_group = group.json()
    json_credits = c_credits.json()
    try:
        c_credits = json_credits['data'][0]['creditos']
        fetched_credits = True
    except:
        c_credits = 0 #if couldn't get credits data
        stringvar.set('No se pudieron obtener los créditos de la clase')
        fetched_credits = False
        
    name = json_name['data'][0]['nombreActividad']
    


    grouplist = json_group['data']
    group_dates = []
    #fetch last horario of grouplist
    stringvar.set('Obtaining Group Dates...')
    for group in grouplist:
        grupid = group['codGrupo']
        grupinfo = requests.get('https://urapprest.uranalytics.p.azurewebsites.net/api/asignaturaDetalle?codigo={0}&opcionDetalle=DetalleFecha&codActividad={0}&codGrupo={1}'.format(code,grupid))
        grupinfo = grupinfo.json()
        group_dates.append( (grupinfo['data'][-1]['fechaInicio'],grupinfo['data'][-1]['fechaFin']) )#save last schedule

    groupinfo = []
    stringvar.set('Fetching Class Blocks info...')
    for i in range(len(grouplist)):
        ini = group_dates[i][0]
        fin = group_dates[i][1]
        grupcod = grouplist[i]['codGrupo']
        r = requests.get('https://urapprest.uranalytics.p.azurewebsites.net/api/asignaturaDetalle?codigo={0}&opcionDetalle=DetalleHorario&codActividad={0}&codGrupo={1}&fechaIni={2}&fechaFin={3}'.format(code,grupcod,ini,fin) )
        groupinfo.append(r.json())

    selectedgroup = groupinfo[(groupid-1)]['data'] #list with blocks
    #print (selectedgroup)
    stringvar.set('Parsing Class Blocks info...')
    teacher = selectedgroup[0]['profesor']
    classinfo = []
    for block in selectedgroup:
        day = block['dia']
        start = block['horaInicio']
        end = block['horaFin']
        start = hr24toampm(start)
        end = hr24toampm(end)
        classinfo.append(day+': '+start+'-'+end)
    if not fetched_credits: warning = 'Nota: No se pudo obtener los créditos de la clase'
    else: warning = ''
    stringvar.set(name+'\n'+'\n'.join(classinfo)+'\n'+warning)
    return (name,teacher,c_credits,classinfo)

class UrosarioPopUp:
    def __init__(self,canvas,classdict,reference_channel):
        self.reference_channel = reference_channel
        reference_channel[0] +=1 #update toplevel ids
        self.canvas = canvas
        self.pre_existant = []
        for key in classdict.keys():
            self.pre_existant.extend(  classdict[key].parse_class_info()   )

       
        
        self.classdict = classdict
        self.window = tk.Toplevel(canvas,takefocus= True)
        self.window.grab_set()
        self.window.geometry('300x300+900+300')
        self.window.title('Añadir de la web...')
        self.window.resizable(False,False)
        
        self.entrycode = tk.Entry(self.window, validate='key', justify= 'right',bg='lightgray')
        self.entrycode['validatecommand'] = (self.entrycode.register(self.codeintcheck),'%P','%d')
        self.entrycode.place(anchor='n',relx=0.5,rely=0.1,relwidth=0.25)

        self.entrygroup = tk.Entry(self.window, validate='key', justify= 'right',bg='lightgray')
        self.entrygroup['validatecommand'] = (self.entrygroup.register(self.groupintcheck),'%P','%d')
        self.entrygroup.place(anchor='n',relx=0.7,rely=0.275,relwidth=0.1)

        self.color = tk.StringVar()
        self.color.set('#ff0000')
        self.colorButton = tk.Button(self.window,text='Color',command=lambda:get_color(self.color,self.colordisplay))
        self.colorButton.place(relx=0.15,rely=0.4,anchor='nw')
        self.colordisplay = tk.Label(self.window,bg=self.color.get(),relief='raised')
        self.colordisplay.place(relx=0.35,rely=0.405,relwidth=0.07,relheight=0.07)

        self.fetchButton = tk.Button(self.window,text='Obtener!',command=lambda:self.fetch_data())
        self.fetchButton.place(relx=0.6,rely=0.4,anchor='nw')

        self.display = tk.StringVar()
        self.label = tk.Label(self.window,textvariable=self.display,bg='lightgray')
        self.label.place(relx=0.1,rely=0.65,relwidth= 0.8,relheight = 0.25)

        self.addbutton = tk.Button(self.window,text='Añadir!',state='disabled',command=lambda: self.send_class_info() )
        self.addbutton.place(anchor='s',relx=0.5,rely=1)
        
        a = tk.Label(self.window,text='Código\n Asignatura ',font=('ComicSans',14))
        a.place(relx=0.1,rely=0.05)
        a = tk.Label(self.window,text='Número de Grupo:  ',font=('ComicSans',14))
        a.place(relx=0.05,rely=0.25)
    def fetch_data(self):
        try:
            self.display.set('Obteniendo Información...')
            self.title,self.teacher,self.c_credits,self.class_blocks = get_class_data(int(self.entrycode.get()),int(self.entrygroup.get()),self.display )
            self.addbutton['state'] = 'normal'
            self.teacher = beauty_string(self.teacher)
            self.title = beauty_string(self.title)
        except:
            self.display.set('No se pudo obtener la información de la clase, intenta de nuevo.')
    def send_class_info(self):
        for blockstring in self.class_blocks:
            if overlap_test(blockstring,self.pre_existant):
                if messagebox.askokcancel("Cruce de Bloques", "Añadir este bloque de clase hara que se cruze con otro, \n ¿Continuar?"):
                    break #keep the code going
                else:
                    return
                
        classinfo_list = []
        for block in self.class_blocks:
            classinfo_list.append(decrypt_classinfo(block))

        createClass(self.canvas,self.classdict,self.title,classinfo_list,self.reference_channel,int(self.c_credits),self.color.get())
        self.classdict[self.title].set_teacher(self.teacher)
        self.window.destroy()
        
    def codeintcheck(self,string,command):
        if len(string) > 8: return False
        if command == '1':
            try:
                int(string)
                return True
            except:
                return False
        return True
    def groupintcheck(self,string,command):
        if command == '1':
            if len(string) > 2: return False
            try:
                n = int(string)
                if n==0: return False
                return True
            except:
                return False
        return True
        
