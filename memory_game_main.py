#Memory Game
#Made by Sam Scott
#10-02-2016
#Python version 3.5.1
#GitHub Repo: https://github.com/Nytra/Memory-Game
__author__ = "Sam Scott <samueltscott@gmail.com>"
from tkinter import *
import random, threading, time, os
try:
    import winsound
except ImportError:
    print("[INFO] Module \"winsound\" failed to load.")
    
#Bugs:
#   None
#ToDo:
#   None

class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.enable_messages = True #Set this to False (With a capital "F") to disable debugging messages in the console
        self.numbers = ["1", "2", "3", "4"]
        self.log_name = "memory_game_log.txt"
        self.check_scorelog()
        try:
            self.path = os.path.abspath("")
        except:
            self.path = None
        self.seq_active = False
        self.started = False
        self.seq_length_boundary = 5
        self.score = 0
        self.num_range = 4
        self.seq_length = self.num_range
        self.create_widgets()
        self.name = "None"
        self.debugging = False
        self.name_ent = Entry(self)
        self.name_ent.grid(row = 5, column = 2, sticky = E)
        self.name_ent.insert(0, "None")
        if self.enable_messages:
            print("[INFO] You can disable these debugging messages by changing self.enable_messages to False on line 22 of the code.")
            print("[INFO] Sequence length: " + str(self.num_range))
            print("[INFO] Score: " + str(self.score))
            print("[INFO] Sequence length boundary: " + str(self.seq_length_boundary))
            print("[INFO] Log name: " + self.log_name)
            if self.path:
                print("[INFO] Path: %s" %self.path)

    def thread_main(self):
        t1 = threading.Thread(target=self.check)
        t1.start()

    def show_sequence(self):
        """Shows the player the sequence by flashing each button red"""
        self.seq_active = True
        self.reset_buttons()
        time.sleep(0.1)
        for x in self.sequence:
            if x == "1":
                self.bttn1["bg"] = "red"
            elif x == "2":
                self.bttn2["bg"] = "red"
            elif x == "3":
                self.bttn3["bg"] = "red"
            else:
                self.bttn4["bg"] = "red"
            time.sleep(0.2)
            self.reset_buttons()
            time.sleep(0.2)
        self.seq_active = False
        self.bttn1["relief"] = "raised"
        self.bttn2["relief"] = "raised"
        self.bttn3["relief"] = "raised"
        self.bttn4["relief"] = "raised"

    def reset_buttons(self):
        self.bttn1["bg"] = "white"
        self.bttn2["bg"] = "white"
        self.bttn3["bg"] = "white"
        self.bttn4["bg"] = "white"
        self.bttn1["relief"] = "sunken"
        self.bttn2["relief"] = "sunken"
        self.bttn3["relief"] = "sunken"
        self.bttn4["relief"] = "sunken"

    def thread_sequence(self):
        """Controls multithreading of the show_sequence function"""
        t2 = threading.Thread(target=self.show_sequence)
        t2.start()

    def start(self):
        """This gets executed when the user clicks the start button
        It will only run if the show_sequence function is done (ie if self.seq_active is False)"""
        
        if not self.seq_active:
            if self.enable_messages:
                print("[EVENT] Button: Start")
            self.name = self.name_ent.get()
            self.thread_beep(500, 100)
            self.started = False
            self.attempt = ""
            self.gen_sequence() #Randomly generates a new sequence
            if self.name == "$dev_user":
                self.debugging = True
                if self.enable_messages:
                    print("[DEBUG] Sequence:", self.sequence)
            self.thread_sequence() #Initiates multithreading of show_sequence()
            self.started =  True
            self.thread_main() #Initiates multithreading of the check() function

    def set_options(self, item, value, targets):
        if not targets:
            for x in self.widgets:
                if x not in exceptions:
                    x[item] = value
        else:
            for x in targets:
                x[item] = value

    def thread_beep(self, pitch, duration):
        try:
            t4 = threading.Thread(target=winsound.Beep, args=(pitch, duration))
            t4.start()
        except:
            pass
                
    def check(self):
        """Checks to see if the attempt matched the generated sequence"""
        while self.started:
            if len(self.attempt) >= self.num_range:
                if self.attempt == self.sequence:
                    self.thread_beep(600, 200)
                    self.thread_beep(800, 200)
                    self.score += 1
                    if self.enable_messages:
                        print("[INFO] Sequence matched!")
                        print("[INFO] Score increased by 1 ({})".format(self.score))
                    if self.score % self.seq_length_boundary == 0 and self.score != 0:
                        self.thread_beep(800, 200)
                        self.thread_beep(1000, 200)
                        self.thread_beep(1200, 200)
                        self.num_range += 1
                        if self.enable_messages:
                            print("[INFO] Sequence length increased by 1 ({})".format(self.num_range))
                        self.sequence_length_lbl["bg"] = "lightgreen"
                    self.started = False
                    self.set_options("bg", "lightgreen", [self.score_lbl, self.bttn1, self.bttn2, self.bttn3, self.bttn4])
                    time.sleep(0.1)
                else:
                    self.thread_beep(400, 200)
                    self.thread_beep(150, 200)
                    if self.enable_messages:
                        print("[INFO] Sequence not matched.")
                    if self.score > 0:
                        self.score -= 1
                        if self.score % self.seq_length_boundary == self.seq_length_boundary - 1:
                            self.num_range -= 1
                            self.thread_beep(170, 200)
                            self.thread_beep(150, 200)
                            self.thread_beep(130, 200)
                            if self.enable_messages:
                                print("[INFO] Sequence length decreased by 1 ({})".format(self.num_range))
                            self.sequence_length_lbl["bg"] = "red"
                        if self.enable_messages:
                            print("[INFO] Score decreased by 1 ({})".format(self.score))
                    self.started = False
                    self.set_options("bg", "red", [self.score_lbl, self.bttn1, self.bttn2, self.bttn3, self.bttn4])
                    time.sleep(0.1)
                self.create_widgets()
                self.configure(background="black")

    def gen_sequence(self): #Generates the sequence
        self.sequence = "".join(random.choice(self.numbers) for x in range(self.num_range))

    def create_widgets(self):                                                                      
        self.bttn1 = Button(self, text = "\n\t1\t\n\n", command = lambda: self.button_press(1), font=("Helvetica", 12, "bold"), bg = "white", relief = SUNKEN) #lambda allows to me pass arguments to the functions
        self.bttn1.grid(row = 1, column = 0, sticky = W)
        self.bttn2 = Button(self, text = "\n\t2\t\n\n", command = lambda: self.button_press(2), font=("Helvetica", 12, "bold"), bg = "white", relief = SUNKEN)
        self.bttn2.grid(row = 1, column = 1, sticky = W)
        self.bttn3 = Button(self, text = "\n\t3\t\n\n", command = lambda: self.button_press(3), font=("Helvetica", 12, "bold"), bg = "white", relief = SUNKEN)
        self.bttn3.grid(row = 2, column = 0, sticky = W)
        self.bttn4 = Button(self, text = "\n\t4\t\n\n", command = lambda: self.button_press(4), font=("Helvetica", 12, "bold"), bg = "white", relief = SUNKEN)
        self.bttn4.grid(row = 2, column = 1, sticky = W)
        self.start_bttn = Button(self, text = "Start", command = self.start, bg = "purple", fg = "white")
        self.start_bttn.grid(row = 3, column = 2, sticky = E)
        self.score_lbl = Label(self, text = "Score: " + str(self.score), bg = "black", fg = "white")
        self.score_lbl.grid(row = 1, column = 2, sticky = E)
        self.sequence_length_lbl = Label(self, text = "Sequence Length: " + str(self.num_range), bg = "black", fg = "white")
        self.sequence_length_lbl.grid(row = 2, column = 2, sticky = E)
        self.info_lbl = Label(self, text = "Copyright Trolley Industries 2016 - All rights reserved", anchor = W, justify = LEFT, bg = "black", fg = "white")
        self.info_lbl.grid(row = 4, column = 2, sticky = E)
        self.name_lbl = Label(self, text = "Name:", bg = "black", fg = "white")
        self.name_lbl.grid(row = 5, column = 2, sticky = W)
        self.widgets = [self.bttn1, self.bttn2, self.bttn3, self.bttn4, self.start_bttn, self.score_lbl, self.sequence_length_lbl, self.info_lbl]

    def check_scorelog(self):
        try:
            with open(self.log_name, "r") as f:
                f.read()
        except FileNotFoundError:
            if self.enable_messages:
                print("[INFO] Creating %s..." %self.log_name)
            with open(self.log_name, "w") as f:
                f.write("Score Log - Created on: " + str(time.ctime(time.time())))
    
    def on_delete(self):
        if self.enable_messages:
            print("[INFO] Interrupted: WM_DELETE_WINDOW")
        self.name = self.name_ent.get()
        if self.name == "":
            self.name = "None"
        if self.enable_messages:
            print("[INFO] Writing to %s..." %self.log_name)
        with open(self.log_name, "a") as f:
            if not self.debugging:
                f.write("\n" + str(time.ctime(time.time())) + " / Name: " + self.name + " - Score: " + str(self.score))
            else:
                f.write("\n" + str(time.ctime(time.time())) + " / Name: $dev_user - Score: " + str(self.score))
        if self.enable_messages:
            print("[INFO] Destroying app...")
        root.destroy()
        if self.enable_messages:
            print("[INFO] Done.")
        
    def button_press(self, num): #Handles button press events
        if self.started:
            if not self.seq_active:
                if self.enable_messages:
                    print("[EVENT] Button:", num)
                self.attempt += str(num)
        else:
            if self.enable_messages:
                print("[EVENT] Buttons are currently disabled")
        

def main():
    global root, app
    root = Tk()
    root.title("Sam's Memory Game V1")
    root.configure(background="black")
    app = Application(root)
    app.configure(background="black")
    root.protocol("WM_DELETE_WINDOW", app.on_delete)
    root.mainloop()

if __name__ == "__main__":
    main()
