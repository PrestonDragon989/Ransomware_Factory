# Ransomware Factory!
The Ransomware Factory is a ✨Magical✨ tool, that produces ransomware based on options you decide in the GUI. It has many options that include: key generation, key storage, self destruction, messages, & and much more! that being said, it should only be used FOR LEARNING, and never illegally!! It can show you a lot of things about basic ransomware. The ransomware made is semi-basic depending on how you build it. It can range from hardly ransomware, to completely functional.
> [!CAUTION]
> Be very careful with all of the code it produces, it may be made simply, but it is still MALWARE


## What can it do?
The Factory can make code based on the following options:
1. Key Method
2. Encryption Method
3. Storage Method
4. Message Type
5. Allow Console
6. File Type
7. Self Destruct
8. Encryption Depth
9. Decryption Type
10. Hide File

It also takes:

- File Name
- Project Name
- Any Message Info
- Email Info if needed

It will then take that code, and then put it into a folder for you. Lets dive into each of the 10 options, to see what you can do.
1. ### Key Method
   The key method can be Fernet, Secrets, or Custom. Each one is just a way to generate a 32 byte URL safe key. They all work with the encryption methods, they are just there for preference.
2. ### Encryption Method
    The Encryption method you choose matters much more than the key method, as this is what encrypts the files. The options are AES (using Fernet) and XOR. AES (Advanced Encryption Standard) is recommended, because it is MUCH more secure than XOR, but XOR is also there in case you want to chose that. XOR (exclusive OR) is simpler, and faster, then fernet. It still uses the same key, and decrypts back to the same data, like AES, so the choice on which one to choose is up to you.
  
3. ### Storage Method
   The storage method, is how you store the key for the encryption/decryption. The options are Key file, ID file, and Email. Key file is where they key is stored in a nearby file, right next to the script. ID file is pretty much the same thing, but the key is encrypted inside. Email is probably the most secure, and the biggest hassle. They key gets emailed to an eamil of your choice, as long as its provided with an email and password to use. Its the biggest hassle to set up. If you are going to use that, I recommend using a burner gmail. With the gmail, you have to go into settings and enable "less secure apps" access, so the python script can access it. Then you have to test it, and maybe trouble shoot it. But when it gets working, it works quite well.

4. ### Message Type
   This is a more simple matter than number 3. This is the type of message you wish to leave when the script finishes. It can be no message, a text file, or a tkinter GUI window. I recommend you use a text file, because it's a bit more stable than the window all around, and more reliable. However, the GUI works just as well. No message is also great. You can put whatever you want in these messages.

5. ### Allow Console
   All this does is toggle output. If you allow it to, it will tell you what its doing, as it does it. If you don't allow it, then it just doesn't tell you. Pretty simple! Leave it off if you have no reason to turn it on, but it you want to try and disect the scripts, and learn how they work, maybe leave it on!

6. ### File Type
   This Defines what type of file it is: A basic python file, or an executable file. If you leave it as a python file, it will have an exstension of .py or .pyw, but if its and executable, than it could either have no exstension (linux) or have .exe (windows). It becomes executable for the OS that you are currently on. If you want it to be executable for a different than you are currently on, then run it in a VM or on a different OS! The choice to have an executable be run via USB is also there, but it only works on windows.

7. ### Self Destruct
   This is another simple one. If you turn this on, it will self destruct when it finishes its code, it self destructs. However, this may conflict with number 9 (Decryption Type), because if you have decrypt and encrypt in one file, it will encrypt then delete itself. So, don't do that! (Unless you want to do that, then I won't judge.)

8. ### Encryption Depth
   This controls what it does, and doesn't encrypt/decrypt. You have 4 options: All below, Current Dir, Only Below, & everything. All below gets all files in the same folder, and all below. Current Dir only gets the files in the same folder, and no files in below folders. Only below only gets files below, and none around. Everything tries to get all files above, around, and below. It may not succeed in getting them all, but it will try. Be warned with that one though, it may take a long time. I recommend All below, you have nice control, with still a broad range.

9. ### Decryption Type
    This dictates whether you have 2 files, one for decyrption, and one for encryption, or just 1 file that does both. The options are Pair, One file (1), and One File (2). Pair is where one file encrypts, and the other decrypts. This is good for mose cases. The decryption file will have "(D)" at the end of its name. One file (1) will encrypt once, and then only decrypt from there. One file (2) will encrypt once, then decrypt once, and then back to encrypt. It will swap between them. You saddly cannot turn a One File into an exe, as the method they use to know when to swap gets broken when they are turned to binary, so you can convert them. Heres a little tip though, the 3rd line of the One files dictates what they do. if it is # ENCRYPT, it encrypts. If it is # DECRYPT, then it decrypts. You can force it to change by changing the code, and swapping them.

10. ### Hide File
    If you enable this, it will attempt to hide itself based on the OS. If it is a Windows OS, then it will try and change it's own permissions. If it is on a Unix based OS, it will add a "." to the beginning of it's name. They can still both be found, but they are a little hidden. It will try to do this after saving the key.

## Where do the Created Files Apear?
If you are running the python files, it will apear in the folder, under the Project Name you gave it. It will be mingling with the other files, so remember what you named it! If you are runnning the Ubuntu version, it should still apear right next to it.

## What is Currently Supported?
It now currently Supports an executable for Ubuntu, and the base Python code. There is instructions on how to install it here in the README, and all it takes is python.
> [!NOTE]
> While there may only be an executable for Ubuntu, its very easy to set up! Even Jonas could do it! (Inside Joke)
## How to Install it with Python?
The factory is bulit soley in Python, and doesn't really use any modules outside of the already included ones. The GUI itself is built with tkinter! The only outside modules used can even be avoided! The two others include: `pyinstaller`, `cryptography`. Pyinstaller is used for the conversion to .exe, and cryptography is used for all scripts that use AES encryption. As long as you have python installed, you will be able to make quite a bit of ransomwares without those two. To get them, all you have to do is go to your command line/terminal, and navigate to the projects directory. Once your there, you can run the following command:
```console
pip3 install -r requirements.txt
```
This will install those two modules for you! How fun! Then, to start the program, all you have to do is type:
```console
python3 main.py
```
This will start the program. All you have to do is run main.py, and boom! You've got the factory! Thats how to run it from the base code. From there, it can do the rest!

## Can I change the colors?
Some people may not like the colors of the factory (I'm not sure if I even like it), so you can change it, in a semi simple way! You have to edit the file `main.py`. All you have to do, is go to the very bottom of the file, and the <b>second to last line</b> of code is what you want to edit. It looks like this:
```python
	app = App(sys.argv[0], '1000', '650', '#f0e6e6', '#281e1e')
```
The `#f0e6e6` is the background color, and the last thing `#281e1e` is the text color. You can replace these to change the colors, but they have to be in hex codes. This will change most of the colors in the factory.
> [!IMPORTANT]
> Make sure to put the new hex codes inbetween the ' ', so it works properly! 
