from scheDefs import * #import very own defs
import tkinter as tk

def open_class_window(canvas,classdict,reference_channel):
    ID = reference_channel[0]
    ID +=1
    reference_channel[0] = ID
    scheduleWindow(canvas,classdict,reference_channel)
#--- /// --- /// --- Setup
string = open('config.cfg','r').read() #sets global lastfile
exec( string )
#print (lastfile,'\n\n\n')

root = tk.Tk()


root.geometry('736x640+100+100') #660 for schedules
root.resizable(False,False)
canvas = tk.Canvas(root)
classdict = {} #this dictionary will keep the title as an identifier of the class and the subject object,so it can be deleted
credits_tracker = tk.IntVar()
credits_tracker.set(0)

show_timestamp = tk.BooleanVar()
show_timestamp.set(pre_timestamp_show)

unsaved = tk.BooleanVar()
unsaved.set(0)

reference_channel = [0,credits_tracker,show_timestamp,1]#,invokebutton] #simple list, allows easy communication between everything, 0 is widget tracker and 1 is n_credits var, 2 bool var of show_timestamp
#fourth is button to use invoke and update root title #0 is for if purposes so that won't call invokebutton on start
''' READ FROM LAST OPENED FILE '''


try:
    file = open(lastfile,'r')   
    file.close()
    open_schedule(lastfile,canvas,classdict,reference_channel)
except:
    error_popup('Could not restore previous schedule, please create new one')
    lastfile = ask_for_new_path()
    if lastfile == '':
        root.destroy() #close
        root.mainloop()
    
    

schedulepath = tk.StringVar()
schedulepath.set(lastfile)

root.title('PyScheduler: '+ lastfile) #title is working schedule

save_state = tk.StringVar()

save_state.set( get_current_save_state(classdict) )
invokebutton = tk.Button(root,command=lambda: process_title_save(root,classdict,save_state,schedulepath,unsaved))
reference_channel.pop(-1)
reference_channel.append(invokebutton)

#global readlist lastpath
''' PROCESS DATA '''
temp = lastfile.split('/')
temp = temp[-1]
temp = temp.strip('.txt')
# --- /// --- /// --- Menu Options
filename = tk.StringVar()
filename.set(temp)
show_title = tk.BooleanVar()
show_title.set(pre_title_show)



root.protocol('WM_DELETE_WINDOW',lambda: on_exit(root,show_title,show_timestamp,schedulepath,unsaved,invoke_save))

title_label = tk.Label(root,textvariable = filename,font=('ComicSans',16))
title_label.place(rely=0,relx=0.5,anchor='n')


update_title_show(show_title,title_label)
update_timestamp_show(show_timestamp,classdict)

invoke_save = tk.Button(command = lambda: save_file(classdict,schedulepath,save_state,invokebutton) )

menubar = tk.Menu(canvas)

filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label="New                    Ctrl+N", command=lambda: new_file(canvas,classdict,unsaved,invoke_save,schedulepath,filename))
root.bind('<Control-n>',lambda event: new_file(canvas,classdict,unsaved,invoke_save,schedulepath,filename) )
filemenu.add_command(label="Open                  Ctrl+O", command=lambda: open_file(canvas,classdict,reference_channel,unsaved,invoke_save,schedulepath,filename) )
root.bind('<Control-o>',lambda event: open_file(canvas,classdict,reference_channel,unsaved,invoke_save,schedulepath,filename))
filemenu.add_command(label="Save                    Ctrl+S", command=lambda: save_file(classdict,schedulepath,save_state,invokebutton))
root.bind('<Control-s>',lambda event: save_file(classdict,schedulepath,save_state,invokebutton) )
filemenu.add_command(label="Save As...    Ctrl+Alt+S", command=lambda: save_as_file(classdict,save_state,invokebutton,filename,schedulepath))
root.bind('<Control-Alt-s>',lambda event: save_as_file(classdict,save_state,invokebutton,filename,schedulepath) )
filemenu.add_separator()
filemenu.add_command(label="Exit", command= lambda: on_exit(root) )

menubar.add_cascade(label="File", menu=filemenu)

showmenu = tk.Menu(menubar,tearoff=0)
showmenu.add_checkbutton(label='Schedule Title',onvalue=1, offvalue=False, variable=show_title,command = lambda: update_title_show(show_title,title_label))
showmenu.add_checkbutton(label='Class Timestamps',onvalue=1, offvalue=False, variable=show_timestamp,command = lambda: update_timestamp_show(show_timestamp,classdict))

menubar.add_cascade(label="Show", menu=showmenu)

newclassButton = tk.Button(root,text='Add Subject',command=lambda: open_class_window(canvas,classdict,reference_channel) )
newclassButton.place(relx=1,rely=0,anchor='ne')#relwidth=0,relheight=)






#Vertical Lines
for i in range(1,7):
    canvas.create_line(((110*i)-30,30),((110*i)-30,630))
#Horizontal Lines
for i in range(1,17):
    canvas.create_line((60,45*i),(736,45*i))
#create timestamps
for i in range(1,17):
    if i >= 6: ampm = 'PM'
    else: ampm = 'AM'
    num = (i+6) % 12
    if (i == 6): num = 12
    #if (i > 6): num +=1
    labeltext = ''
    labeltext += str(num)
    labeltext += ':00'
    labeltext += ampm
    a = tk.Label(canvas,text=labeltext,font=('ComicSansBold',11))
    a.place(relx=0,rely = 0.07*i,anchor = 'w')













canvas.place(relx = 0,rely=0.05,relwidth=1,relheight=1)
credits_display = tk.Label(root,textvariable = credits_tracker,font=('ComicSansBold',12) )
credits_display.place(rely=0,relx=0.14)

urosario_fetch = tk.Button(root,text='Add from Database...',command= lambda: UrosarioPopUp(canvas,classdict,reference_channel) )
urosario_fetch.place(rely=0,relx=0.8,anchor='n')

label = tk.Label(root,text='Total Credits:',font=('ComicSans',12))
label.place(rely=0,relx=0)
label = tk.Label(canvas,text=' Monday      Tuesday Wednesday   Thursday      Friday      Saturday',font=('ComicSans',16))
label.place(rely=0,relx=0.125,anchor='nw')

#test_button = tk.Button(text='Press me',command= lambda: print( difference_check(classdict,save_state) )       )
#test_button = tk.Button(text='Press me',command= lambda: print(asksave(root,canvas,reference_channel) )      )
#test_button.place(relx=0.5,rely=0.5)

root.config(menu=menubar)
root.mainloop()


