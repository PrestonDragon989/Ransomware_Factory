class Profile:
    def __init__(self):
        # Ransomware Details
        self.key_method = "Fernet key" 
        self.encryption_method = "AES" 
        self.storage_method = "Key File" 
        self.message_type = "None"
        self.show_console = "No" 
        self.file_type = ".py" 
        self.self_destruct = "No" 
        self.encryption_depth = "All Below" 
        self.decryption_type = "Pair"
        self.hide_file = "No"

        # Init Data
        self.file_name = "ransomware" # Done
        self.project_name = "Ransomware" # Done

        # Email Data
        self.from_email = ""
        self.from_password = ""
        self.to_email = ""

        # Message Data
        self.GUI_type = 1
        self.GUI_message = ["Text 1", "Text 2", "Text 3", "Text 4", "https://www.google.com/"]
        self.text_file = "R\\n\\tA\\n\\t\\tN\\n\\t\\t\\tS\\n\\t\\t\\t\\tO\\n\\t\\t\\t\\t\\tM\\n>:3"