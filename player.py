from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk


root = Tk()

root.title("MP3 Player")
root.geometry("500x400")

#initaialize Pygame
pygame.mixer.init()

#function to deal time
def play_time():
	#check if song stopped
	if stopped:
		return
	current_time=pygame.mixer.music.get_pos()/1000
	converted_current_time=time.strftime('%M:%S',time.gmtime(current_time))

	#current song length
	song = playlist_box.get(ACTIVE)
	song = f'D:/mp3/audio/{song}.mp3'

	song_mut=MP3(song)
	global song_length
	song_length = song_mut.info.length
	#convert to time format
	converted_song_length= time.strftime('%M:%S',time.gmtime(song_length))

	if int(song_slider.get())== int(song_length):
		stop()

	elif paused:
		pass

	else:
		#move slider along 1 second 
		next_time = int(song_slider.get())+1
		#output new time value to slider
		song_slider.config(to=song_length, value=next_time)

		#convert slider position to time format
		converted_current_time= time.strftime('%M:%S',time.gmtime(int(song_slider.get())))

		#set slider
		status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}   ')

	if current_time > 0:
		#add time to staatus bar
		status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}   ')
	#loop to show time after each sec
	status_bar.after(1000,play_time)

#fuction to add one song to playlist
def add_song():
	song=filedialog.askopenfilename(initialdir='audio/', title="Choose a Song", filetypes=(("mp3 Files", "*.mp3"), ))
	#my_label.config(text=song)
	song =song.replace("D:/mp3/audio/","")
	song=song.replace(".mp3","")
	playlist_box.insert(END,song)

#function to add many song to playlist
def add_many_songs():
	songs=filedialog.askopenfilenames(initialdir='audio/', title="Choose a Song", filetypes=(("mp3 Files", "*.mp3"), ))

	for song in songs:
		#add song to list
		song =song.replace("D:/mp3/audio/","")
		song=song.replace(".mp3","")
		playlist_box.insert(END,song)

#function to delete a song from playlist
def delete_song():
	playlist_box.delete(ANCHOR)

#function to delete many song from playlist
def delete_all_songs():
	playlist_box.delete(0,END)

#play function
def play():
	#set stopped to false
	global stopped
	stopped=False
	song = playlist_box.get(ACTIVE)
	song = f'D:/mp3/audio/{song}.mp3'
	
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	#get song time
	play_time()

#stopped variable
global stopped
stopped = False
#stop fuction
def stop():
	pygame.mixer.music.stop()
	#clear active song
	playlist_box.selection_clear(ACTIVE)

	status_bar.config(text='')

	song_slider.config(value=0)

	global stopped
	stopped = True

# Fuction to play next song
def next_song():
	#reset status bar and slider
	status_bar.config(text='')
	song_slider.config(value=0)
	#get current song no
	next_one= playlist_box.curselection()
	next_one=next_one[0]+1
	#get song title of next song
	song=playlist_box.get(next_one)
	song = f'D:/mp3/audio/{song}.mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	#clear active song
	playlist_box.selection_clear(0,END)
	#move active bar to next song
	playlist_box.activate(next_one)
	#set active bar to next song
	playlist_box.selection_set(next_one,last=None)

#function to play pervious song
def previous_song():
	#reset status bar and slider
	status_bar.config(text='')
	song_slider.config(value=0)
	#get current song no
	next_one= playlist_box.curselection()
	next_one=next_one[0]-1
	#get song title of next song
	song=playlist_box.get(next_one)
	song = f'D:/mp3/audio/{song}.mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	#clear active song
	playlist_box.selection_clear(0,END)
	#move active bar to next song
	playlist_box.activate(next_one)
	#set active bar to next song
	playlist_box.selection_set(next_one,last=None)

#paused var
global paused
paused=False

#create pause function
def pause(is_paused):
	global paused
	paused= is_paused

	if paused:
		pygame.mixer.music.unpause()
		paused=False
	else:
		pygame.mixer.music.pause()
		paused=True

#create volume function
def volume(x):
	pygame.mixer.music.set_volume(volume_slider.get()) 

#slider function
def slide(x):
	#to slide to particular time
	song = playlist_box.get(ACTIVE)
	song = f'D:/mp3/audio/{song}.mp3'
	
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0,start=song_slider.get())
	

#Create  main frame
main_frame= Frame(root)
main_frame.pack(pady=20)

# to create a playlist box
playlist_box = Listbox(main_frame, bg="black", fg="green",width=60, selectbackground="green", selectforeground="black")
playlist_box.grid(row=0, column=0)

#volume slider frame
volume_frame= LabelFrame(main_frame,text='Volume')
volume_frame.grid(row=0 ,column=1, padx=15)

#create volume slider
volume_slider= ttk.Scale(volume_frame, from_=0, to=1,orient= VERTICAL, length=125,value=1,command=volume)
volume_slider.pack(pady=10)

#song slider
song_slider = ttk.Scale(main_frame, from_=0, to=100,orient= HORIZONTAL, length=357,value=0,command=slide)
song_slider.grid(row=2,column=0,pady=20)

#define button images for control
back_btn_img=PhotoImage(file='images/back50.png')
forward_btn_img=PhotoImage(file='images/forward50.png')
play_btn_img=PhotoImage(file='images/play50.png')
pause_btn_img=PhotoImage(file='images/pause50.png')
stop_btn_img=PhotoImage(file='images/stop50.png')


# create buttons frame
control_frame = Frame(main_frame)
control_frame.grid(row=1,column=0,pady=20)

# create play/pause button
back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(control_frame, image=forward_btn_img,borderwidth=0, command=next_song)
play_button = Button(control_frame, image=play_btn_img,borderwidth=0,command=play)
pause_button = Button(control_frame, image=pause_btn_img,borderwidth=0,command=lambda: pause(paused) )
stop_button = Button(control_frame, image=stop_btn_img,borderwidth=0,command=stop )

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4,padx=10)

#create menu

my_menu = Menu(root)
root.config(menu=my_menu)

#create Add song Menu Dropdowns
add_song_menu = Menu(my_menu,tearoff=0)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
#add one song to playlist 
add_song_menu.add_command(label="Add one song to Playlist", command=add_song)
#add many song to playlist 
add_song_menu.add_command(label="Add many songs to Playlist", command=add_many_songs)
#create Delete Song menu Dropdown
remove_song_menu=Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove Songs",menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a song from playlist", command=delete_song)
remove_song_menu.add_command(label="Delete all songs from playlist", command=delete_all_songs)

#status bar
status_bar= Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X,side=BOTTOM, ipady=2)


#Temporary label
my_label = Label (root,text= '')
my_label.pack(pady=20)



root.mainloop()