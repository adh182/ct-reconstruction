from tkinter import *
import tkinter.ttk as ttk 
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import filedialog
from tkinter import messagebox
from skimage import io
from CTProgram import CT
import os

class Window:

	def __init__(self, master):
		'''Initialize window'''

		self.master = master
		self.init_window()

	def init_window(self):
		'''Collect all method in a single window'''

		self.master.title("Computed Tomography Reconstruction")
		self.fontstyle1 = ('Courier', 17, 'bold')
		self.fontstyle2 = ('Courier', 12, 'bold')
		self.fontstyle3 = ('Times New Roman', 11)
		self.fontstyle4 = ('Times New Roman', 12)
		self.make_frame()
		self.title()
		self.frame_1()
		self.frame_2()
		self.frame_3()
		self.frame_4()

	def make_frame(self):
		'''Make four frames'''

		self.frame1 = Frame(height=340, width=460, borderwidth=3, relief=FLAT)
		self.frame2 = Frame(height=340, width=460, borderwidth=3, relief=FLAT)
		self.frame3 = Frame(height=340, width=460, borderwidth=3, relief=FLAT)
		self.frame4 = Frame(height=340, width=460, borderwidth=3, relief=FLAT)

		self.frame1.place(x=11, y=10)
		self.frame2.place(x=485, y=10)
		self.frame3.place(x=11, y=360)
		self.frame4.place(x=485, y=360)

	def title(self):
		'''Make title: Computed Tomography Reconstruction'''

		title = Label(self.frame1, text="COMPUTED TOMOGRAPHY \nRECONSTRUCTION", font=self.fontstyle1, fg='#465a62')
		# title.place(x=140, y=5)
		title.place(x=100, y=5)

	def frame_1(self):
		'''Frame 1 - all the input needed'''

		style = ttk.Style()
		style.configure('TButton', font=self.fontstyle3, bg='dark blue', width=10)
		image_button = ttk.Button(self.frame1, text="Load Image", style='TButton', width=15, command=self.load_image_command)
		image_button.place(x=195, y=250)

		calculate_button = ttk.Button(self.frame1, text='Calculate', style='TButton', width=15, command=self.calculate_command)
		calculate_button.place(x=320, y=250)

		clear_button = ttk.Button(self.frame1, text='Clear', style='TButton', width=15, command=self.clear)
		clear_button.place(x=320, y=290)

		save_button = ttk.Button(self.frame1, text='Save', style='TButton', width=15, command=self.save)
		save_button.place(x=195, y=290)

		lbl_max_angle = Label(self.frame1, text='Maximum Angle		: ', font=self.fontstyle3)
		lbl_max_angle.place(x=20, y=90)

		lbl_reconstruction = Label(self.frame1, text='Reconstruction Method	: ', font=self.fontstyle3)
		lbl_reconstruction.place(x=20, y=120)

		lbl_filter = Label(self.frame1, text='Filter Type		: ', font=self.fontstyle3)
		lbl_filter.place(x=20, y=150)

		lbl_num_proj = Label(self.frame1, text='Number of projection	: ', font=self.fontstyle3)
		lbl_num_proj.place(x=20, y=180)

		#combobox method
		method_name = ['Filtered Back Projection', 'SART']

		#combobox filter
		filter_name = ['ramp', 'shepp-logan', 'cosine', 'hamming', 'hann']

		style.map('TCombobox', fieldbackground=[('readonly', 'lightblue')])
		style.map('TCombobox', background=[('readonly', 'lightblue')])
		style.map('TCombobox', foreground=[('readonly', 'black')])

		self.txt_angle = Text(self.frame1, width=25, height=1, font=self.fontstyle3)
		self.txt_angle.place(x=200, y=90)

		cmb_methodVar = StringVar()
		self.cmb_method = ttk.Combobox(self.frame1, textvariable='cmb_methodVar', font=self.fontstyle4)
		self.cmb_method['values'] = method_name
		self.cmb_method['state'] = 'readonly'
		self.cmb_method.current(0)
		self.cmb_method.place(x=200, y=120)

		cmb_filterVar = StringVar()
		self.cmb_filter = ttk.Combobox(self.frame1, textvariable='cmb_filterVar', font=self.fontstyle4)
		self.cmb_filter['values'] = filter_name
		self.cmb_filter['state'] = 'readonly'
		self.cmb_filter.current(0)
		self.cmb_filter.place(x=200, y=150)

		self.lbl_proj = Label(self.frame1, text='0 projections', font=self.fontstyle3)
		self.lbl_proj.place(x=200, y=180)

		#Radiobutton
		self.release = IntVar()
		self.release.set(1)
		ticks_rbutton1 = ttk.Radiobutton(self.frame1, text='Show image size', variable=self.release, value=1)
		ticks_rbutton1.place(x=20, y=270)
		
		ticks_rbutton2 = ttk.Radiobutton(self.frame1, text='Hide image size', variable=self.release, value=2)
		ticks_rbutton2.place(x=20, y=295)

	def frame_2(self):
		'''Frame 2 - for original image'''

		frame2_title = Label(self.frame2, text="Original Image", font=self.fontstyle2, fg='black')
		frame2_title.place(x=165, y=5)

		self.canvas_list = []
		
	def frame_3(self):
		'''Frame 3 - for sinogram'''

		frame3_title = Label(self.frame3, text="Sinogram", font=self.fontstyle2, fg='black')
		frame3_title.place(x=180, y=5)
 
	def frame_4(self):
		'''Frame 4 - for reconstruction image'''

		frame4_title = Label(self.frame4, text="Reconstruction", font=self.fontstyle2, fg='black')
		frame4_title.place(x=165, y=5)

	def load_image(self, image):
		'''Load original image'''

		img = CT(image, 180, "hann")
		rescaled_image, __, __ = img.process_image()
		fig, ax = plt.subplots(1,1, figsize=(3, 3))

		#Remove image size if Hide image size radiobutton selected
		if self.release.get() == 2:
			plt.tick_params(left = False, right = False , labelleft = False ,
	                		labelbottom = False, bottom = False)

		ax.imshow(rescaled_image, cmap=plt.cm.Greys_r)
		self.canvas_original = FigureCanvasTkAgg(fig, master=self.frame2)
		self.canvas_original.draw()
		self.canvas_original.get_tk_widget().place(x=80, y=30)

		#Add canvas to the canvas list
		self.canvas_list.append(self.canvas_original.get_tk_widget())
		
	def load_image_command(self):
		'''Load image button command'''

		filename = filedialog.askopenfilename()
		try:
			self.image = io.imread(str(filename))
		except:
			messagebox.showinfo('Wrong format', 'Unsupported file extension.\nTry image in .png or .jpeg')

		self.load_image(self.image)

	def calculate(self):
		'''Calculate sinogram and reconstruction image'''

		img = self.image
		theta = int(self.txt_angle.get("1.0", "end"))
		filter_type = self.cmb_filter.get() 

		#Call original image - update the state if Hide image size radiobutton selected 
		self.load_image(img)

		self.ct_img = CT(img, theta, filter_type)
		sinogram = self.ct_img.radon_transform()
		reconstruction = self.ct_img.filtered_back_projection()

		#check if reconstruction method is SART
		if self.cmb_method.current == 'SART':
			reconstruction = self.ct_img.sart()

		__, __, num_projection = self.ct_img.process_image()
		self.lbl_proj.config(text = str(num_projection)+' projections')

		#create sinogram graph
		fig1, ax1 = plt.subplots(1,1, figsize=(3, 3))

		#Remove image size if Hide image size radiobutton selected
		if self.release.get() == 2:
			plt.tick_params(left = False, right = False , labelleft = False ,
                			labelbottom = False, bottom = False)

		ax1.imshow(sinogram, cmap=plt.cm.Greys_r)
		self.canvas_sinogram = FigureCanvasTkAgg(fig1, master=self.frame3)
		self.canvas_sinogram.draw()
		self.canvas_sinogram.get_tk_widget().place(x=80, y=30)

		#Add canvas to the canvas list
		self.canvas_list.append(self.canvas_sinogram.get_tk_widget())

		#create reconstruction graph
		fig2, ax2 = plt.subplots(1,1, figsize=(3, 3))

		#Remove image size if Hide image size radiobutton selected
		if self.release.get() == 2:
			plt.tick_params(left = False, right = False , labelleft = False ,
	                		labelbottom = False, bottom = False)

		ax2.imshow(reconstruction, cmap=plt.cm.Greys_r)
		self.canvas_recons = FigureCanvasTkAgg(fig2, master=self.frame4)
		self.canvas_recons.draw()
		self.canvas_recons.get_tk_widget().place(x=80, y=30)

		#Add canvas to the canvas list
		self.canvas_list.append(self.canvas_recons.get_tk_widget())

	def calculate_command(self):
		'''Calculate button command'''

		try:
			self.calculate()
		except:
			messagebox.showerror('Error', 'Required input unspecified')

	def clear(self):
		'''Clear button command - to clear all the results'''

		self.canvas_original.get_tk_widget().destroy()
		self.canvas_sinogram.get_tk_widget().destroy()
		self.canvas_recons.get_tk_widget().destroy()
		self.lbl_proj.config(text = '0 projections')

		for canvas in self.canvas_list:
			canvas.destroy()

	def save(self):
		'''Save button command - to save graph as png file'''

		file = filedialog.asksaveasfile(mode='w', filetypes=[('PNG Image', '*.png')], defaultextension='.*')

		if file is None:
			'''If user cancels'''
			return
		
		file.close()
		fig = self.ct_img.graph()
		fig.set_size_inches(8, 8)
		os.remove(file.name)
		print("Saving png file. . .")
		plt.savefig(file.name)


root = Tk()
app = Window(root)
root.geometry("960x720")
root.resizable(0,0)
root.configure(bg='#c9d0d3')
root.mainloop()