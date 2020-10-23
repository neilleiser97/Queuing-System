#Name: Neil Leiser
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import filedialog
import time

class App(object):
    """ A queueing application """
    
    def __init__(self, master):
        """ 
        Create queue application

        Parameters:
        master(tk.Tk()): main window
        """
        self._master=master
        self._master.title("CSSE1001 Queue")
        self._master.geometry('1140x800') #Can set the geometry to '1500x800' on a uni computer to have a better overview of the queue

        #Menu used to access the game
        menubar = tk.Menu(self._master)
        self._master.config(menu=menubar)
        newmenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=newmenu)
        newmenu.add_command(label="Tic Tac Toe", command=self.new_game)
        
        #Top Part
        #Top Frame
        self._top_frame = tk.Frame(self._master,bg="floral white")
        self._top_frame.pack(side=tk.TOP,fill=tk.X)
        
        #Label 1 Title
        self._title_top = tk.Label(self._top_frame,justify=tk.LEFT,padx = 20, text= top_label_title,bg="floral white",font='Arial 16 bold',fg ='Orange')
        self._title_top.pack(side=tk.TOP,anchor=tk.W,pady=5)
        
        #Label 1 Text
        self._text_top = tk.Label(self._top_frame,justify=tk.LEFT,padx = 20, text= top_label_text,bg="floral white")
        self._text_top.pack(side=tk.TOP,anchor=tk.NW,ipady=10,pady=5)
        
        #Left Major Frame for quick queue
        self._frame_quick = tk.Frame(self._master)
        self._frame_quick.pack(side=tk.LEFT,anchor = tk.N)

        #Right Major Frame for long queue
        self._frame_long = tk.Frame(self._master)
        self._frame_long.pack(side=tk.RIGHT,anchor = tk.N)
        
        #Create two Labels one for quick and one for long questions
        BigLabel(self._frame_quick,quick_question_title,quick_question_text,quick_question_bg,quick_question_fg)
        BigLabel(self._frame_long,long_question_title,long_question_text,long_question_bg,long_question_fg)
        
        #Create examples for quick and long questions
        Example(self._frame_quick, quick_example_text)
        Example(self._frame_long, long_example_text)

        #Create main buttons
        self._quick_button = Button(self._frame_quick, 'darkgreen', quick_button_text, 'lightgreen',self.redraw_quick)
        self._long_button = Button(self._frame_long, 'darkblue', long_button_text, 'lightblue',self.redraw_long)
               
        #Top Grid
        self._quick_grid = TopGrid(self._frame_quick)
        self._long_grid = TopGrid(self._frame_long)

        #Create label that describes number of students and average wait time of queue
        self.queue_label()
        
    def new_game(self):
        """
        Function used to call the Tic-Tac-Toe game
        """
        root2 = tk.Toplevel()
        game = Game(root2)
        root2.mainloop()
        
    def queue_label(self):
        """
        Creates label which describes number of students and average wait time in queue
        """
        self._quick_grid.set_label()
        self._long_grid.set_label()
        self._master.after(1000,self.queue_label) #Refresh every second
        
    def redraw_quick(self):
        """
        Updates quick queue view and quick queue model
        """
        dialog_box = simpledialog.askstring("Input","Enter your first and last name",parent=self._quick_button.get_button())

        if dialog_box == None: #if student presses cancel, he is not added to the queue
            return
        
        else:
            student1 = Student(self._quick_grid.get_queue(),dialog_box)
            if (student1.get_name() not in self._long_grid.get_model().name_active_students()): #Check if student is already in the other queue
                if (self._quick_grid.get_model().add_student(student1)):
                    self._quick_grid.get_queue().add_row(student1)
                    self._quick_grid.get_queue().refresh_grid()
                
    def redraw_long(self):
        """
        Updates long queue view and quick queue model
        """
        dialog_box = simpledialog.askstring("Input","Enter your first and last name",parent=self._long_button.get_button())

        if dialog_box == None:#if student presses cancel, he is not added to the queue
            return
        
        else:
            student1 = Student(self._long_grid.get_queue(),dialog_box)
            if (student1.get_name() not in self._quick_grid.get_model().name_active_students()): #Check if student is already in the other queue
                if(self._long_grid.get_model().add_student(student1)):
                    self._long_grid.get_queue().add_row(student1)
                    self._long_grid.get_queue().refresh_grid()
        
class QueueModel():
    """A Model of the queue"""

    def __init__(self):
        """
        Construct a queue model
        """
        self._students = {}
        self._active_students = [] #Students currently in the queue

    def add_student(self,student):
        """
        Adds a student to the queue

        parameter:
        student(Student): student to be added to the queue

        Returns:
        bool: True if the student can join the queue
        and False if the student is already in the queue
        """
        for name,stud in self._students.items():
            if (name == student.get_name()) and stud[0].get_state(): #check if student is in the queue
                return False
            elif student.get_name() == stud[0].get_name(): #check if student has been in the queue before to update its number of questions asked
                student.set_question(stud[0].get_question()+1)
                student.update_values()
                
        self._students.update({student.get_name():[student,student.get_question()]}) #add or update student details
        return True
        
    def get_students(self):
        """
        returns students that have registered in the queue
        
        Returns:
        dict: A dictionary of students that are or have been in the queue (key = name(str), items = [student(Student), questions asked(int)])
        """
        return self._students
    
    def get_active_students(self):
        """
        Returns:
        List(Students): returns a list of students that are currently in the queue
        """
        self._active_students = []
        for name, stud in self._students.items():
            if stud[0].get_state():
                self._active_students.append(stud[0])

        self._active_students.sort(key=lambda x: x._time,reverse = True) #priority to students who have waited longer
        self._active_students.sort(key=lambda x: x._question) #priority to students who have asked less questions

        return self._active_students
    
    def name_active_students(self):
        """
        Returns:
        List: returns a list of names(str) of students that are currently in the queue
        """
        name = []
        for stud in self._active_students:
            name.append(stud.get_name())
        return name
    
    def len_queue(self):
        """
        Returns:
        int: number of students in the queue
        """
        return len(self._active_students)
    
    def average_time(self):
        """
        Returns:
        float: average wait time in the queue
        """
        sum_time = 0
        for stud in self._active_students:
            sum_time += stud.get_time()
        av_time = sum_time/len(self._active_students)
        return av_time
    
    def refresh(self):
        """
        Gives a general overview of the queue

        Returns:
        str: The average wait time and number of students in the queue
        """
        if self.len_queue() == 0:
            return 'No students in queue.'
        elif (self.average_time() < 60) and (self.len_queue() == 1):
            return 'An average wait of a few seconds for one student'
        elif (self.average_time() < 60) and (self.len_queue() > 1):
            return 'An average wait of a few seconds for {} students'.format(self.len_queue())
        elif self.average_time() < 120 and (self.len_queue() == 1):
            return 'An average wait of about one minute for one student'
        elif (self.average_time() < 120) and (self.len_queue() > 1):
            return 'An average wait of about one minute for {} students'.format(self.len_queue())
        elif self.average_time() < 3600 and (self.len_queue() == 1):
            return 'An average wait of about {} minutes for one student'.format(int(self.average_time()/60))
        elif self.average_time() < 3600 and (self.len_queue() > 1):
            return 'An average wait of about {} minutes for {} students'.format(int(self.average_time()/60),self.len_queue())
        elif self.average_time() < 7200 and (self.len_queue() == 1):
            return 'An average wait of about one hour for one student'
        elif self.average_time() < 7200 and (self.len_queue() > 1):
            return 'An average wait of about one hour for {} students'.format(self.len_queue())
        elif self.average_time() >= 7200 and (self.len_queue() == 1):
            return 'An average wait of about {} hours for one students'.format(int(self.average_time()/3600))
        else:
            return 'An average wait of about {} hours for {} students'.format(int(self.average_time()/3600),self.len_queue())


class QueueView(tk.Frame):
    """A Tkinter grid which represents the queue"""
    def __init__(self, master, columns, model, *args, **kwargs):
        """
        Construct a new grid

        Parameters:
            master (tk.Frame): Frame containing this widget
            columns (int): Amount of columns in the grid
            model (Model): Model of the queue (backend)
        """
        super().__init__(master, *args, **kwargs)
        self._master = master
        self._model = model
        self._row = 0

        # configure the grid to fill the space
        for column in range(columns):
            tk.Grid.columnconfigure(self, column, weight=1)

    def get_row(self):
        """
        Returns:
        int: index number of the first empty row
        """
        return self._row
            
    def add_column(self, values,fonts=None):
        """
        Adds columns to the grid

        Parameters:
        values (List): List of column headers
        fonts (str): Font used for the column headers
        """
        for column, value in enumerate(values):
            label = tk.Label(self, text=value,font=fonts)
            label.grid(row=self._row, column=column, sticky=tk.W)
        self._row += 1
        
    def add_row(self, student,fonts=None):
        """
        Append a new row of values to the grid

        Parameters:
            student (Student): Student that is added to the row
            fonts (str): Font used 
        """
        values = student.get_items() #get student's details
    
        for column, value in enumerate(values):
            if column <4: #Add labels
                label = tk.Label(self, text=value,font=fonts)
                label.grid(row=self._row, column=column, sticky=tk.W)
                
            else: #Add buttons
                value.grid(row=self._row, column=column, sticky=tk.W)              

        self._row += 1

    def refresh_grid(self):
        """
        Deletes the entire grid and then updates it (every 10 sec)
        """
        self.after(10000,self.refresh_grid) 
        for label in self.grid_slaves(): #delete the grid
            if int(label.grid_info()["row"]) >= 1:
                label.grid_forget()
                
        self._row = 1
    
        for student in self._model.get_active_students(): #update the grid
            student.update_time()
            student.set_number(self._row)
            student.update_values()
            self.add_row(student)

class Student():
    """
    A Student that joins the queue
    """
    def __init__(self,master,name):
        """
        Create a student

        Parameters:
        master (tk.Grid): Queue where the student is added
        name(str): Student's name
        """
        self._name = name
        self._master = master
        self._number = self._master.get_row() #row number
        self._start_time = time.time()
        self._time = time.time()-self._start_time #waiting time
        self._question = 0
        #Associate student whith buttons
        self._red_button = tk.Button(master,highlightbackground='red',command = self.remove_student_red)
        self._green_button = tk.Button(master,highlightbackground='green',command = self.remove_student_green)
        #Students details needed
        self._values = [self.get_number(),self.get_name(),self.get_question(),self.get_string_time(),self._red_button,self._green_button]
        self._state = True 

    def set_state(self):
        """
        Changes the "state" of the student
        If state is True, the student is active in the queue
        If state is False, student is not active in the queue
        """
        self._state = not self._state        

    def get_state(self):
        """
        Returns the "state" of the student

        Returns:
        bool: True if student is active and False if he is not
        """
        return self._state
    
    def update_time(self):
        """
        Updates the waiting time of the student
        """
        self._time = time.time() - self._start_time
        
    def update_values(self):
        """
        Updates student's details
        """
        self._values = [self.get_number(),self.get_name(),self.get_question(),self.get_string_time(),self._red_button,self._green_button]
        
    def get_time(self):
        """
        Returns the amount of time the student has been waiting in a queue

        Returns:
        float: waiting time of the student (in seconds)
        """
        return self._time
    
    def get_string_time(self):
        """Returns the amount of time the student has been waiting

        Returns:
        str: waiting time of student
        """
        if self._time < 60:
            string_time = "a few seconds ago"
        elif self._time < 120:
            string_time = "a minute ago"
        elif self._time < 3600:
            string_time = "{} minutes ago".format(int(self._time/60))
        elif self._time < 7200:
            string_time = "an hour ago"
        else:
            string_time = "{} hours ago".format(int(self._time/3600))
            
        return string_time
    
    def set_question(self, num):
        """
        Sets the number of answered questions

        Parameters:
        num (int): number of answered questions
        """
        self._question = num

    def get_question(self):
        """
        Returns the number of answered questions for a student

        Returns:
        int: number of answered questions
        """
        return self._question
    
    def get_name(self):
        """
        Returns the name of a student

        Returns:
        str: name of student
        """
        return self._name
    
    def set_number(self,num):
        """
        Sets row number of a student in the queue

        Parameters:
        num (int): Student's row number
        """
        self._number = num

    def get_number(self):
        """
        Returns the row number of a student

        Returns:
        int: Student's row number
        """
        return self._number
    
    def get_items(self):
        """
        Returns student's details that will be displayed in the grid

        Returns:
        List: Student's details
        """
        return self._values
    
    def remove_student_red(self):
        """
        Removes a student from the queue without changing the number of answered questions
        """
        self._question -= 1
        self._state = False
        self._master.refresh_grid()

    def remove_student_green(self):
        """
        Removes a student from the queue
        The number of questions answered for this student will increase by 1
        """
        self._state = False
        self._master.refresh_grid()
        
class BigLabel():
    """
    A Label that describes the queue
    """
    def __init__(self,master,title,time_text,colour_bg,colour_fg):
        """
        Create a label

        Parameters:
        master (tk.Frame): Main Frame containing the label
        title (str): Name of the queue
        time_text (str): Queue description
        colour_bg (str): Background color of label
        colour_fg (str): Text colour
        """
        self._master = master
        self._title = title
        self._time_text = time_text
        self._colour_bg = colour_bg
        self._colour_fg = colour_fg
        
        #Use a frame and add two labels (same for long questions)
        self._frame = tk.Frame(self._master,bg=self._colour_bg)
        self._frame.pack(side=tk.TOP,padx=20,pady=20)
        self._text1 = tk.Label(self._frame,text=self._title,bg=self._colour_bg,font = 'Arial 22 bold', fg = self._colour_fg)
        self._text1.pack(side=tk.TOP,ipadx=170,pady=20)
        self._text2 = tk.Label(self._frame,text=self._time_text,bg=self._colour_bg)
        self._text2.pack(side=tk.TOP,ipadx=170,pady=20)
        
class Example():
    """
    Create example for the queue (quick and long questions)
    """
    def __init__(self,master,text):
        """
        Create label with example of questions for the queue

        Parameters:
        master (tk.Frame): Frame containing this label
        text (str): List of examples 
        """
        self._master = master
        self._text = text
        self._label = tk.Label(self._master,justify = tk.LEFT,text=self._text,anchor = tk.W)
        self._label.pack(side=tk.TOP,padx = 20, anchor = tk.W)
        
class Button():
    """
    Create a button 
    """
    def __init__(self, master, master_bg, text, bg, command):
        """
        Create a button

        Parameters:
        master (tk.Frame): Main frame containing this button
        master_bg (str): Background colour of the small frame containing this button
        text (str): text of the button
        bg (str): Background colour of the button
        command (function): Function associated with the button
        """
        self._master = master
        self._master_bg = master_bg
        self._text = text
        self._bg = bg
        self._command = command
        
        
        self._frame = tk.Frame(self._master,bg = self._master_bg)
        self._frame.pack(side = tk.TOP)
        self._button = tk.Button(self._frame, text = self._text,fg = "white",highlightbackground = self._bg, command = self._command)
        self._button.pack()
    
    def get_button(self):
        """
        Returns the button

        Returns:
        tk.Button: the button
        """
        return self._button

class TopGrid():
    """
    Create top part of the Grid (queue)
    """
    def __init__(self,master):
        """
        Create top part of the queue

        Parameters:
        master (tk.Frame): Main frame containing this grid
        """
        self._master = master
        self._frame_bg = tk.Frame(self._master,bg='grey')
        self._frame_bg.pack(side=tk.TOP,fill = tk.X,pady=5,padx=20)
        self._frame_overview = tk.Frame(self._frame_bg)
        self._frame_overview.pack(side=tk.TOP,fill=tk.X,pady=1)
        self._model = QueueModel()
        self._label = tk.Label(self._frame_overview,height=3,justify = tk.LEFT,text = self._model.refresh())
        self._label.pack(side=tk.LEFT)
        self._grid = QueueView(self._frame_bg,6,self._model)
        self._grid.pack(side=tk.LEFT,anchor='n')
        self._grid.add_column(("#      ","Name                   ","Questions Asked      ","Time                             ","     ","     "),'Arial 16 bold')
    
    def set_label(self):
        """
        Updates the label which gives information on the number of students in the queue and average wait time
        """
        self._label.destroy()
        self._label = tk.Label(self._frame_overview,height=3,justify = tk.LEFT,text = self._model.refresh())
        self._label.pack(side=tk.LEFT)
        
    def get_queue(self):
        """
        Returns the queue (bottom grid) associated with this top grid

        Returns:
        QueueView: the Queue associated with the top grid
        """
        return self._grid
    
    def get_model(self):
        """
        Returns the model (backend) of the queue

        Return:
        QueueModel: the model associated with this grid
        """
        return self._model


########## EXTENSION: TIC-TAC-TOE GAME ##########
    
class Game(object):
    """
    A game of Tic-Tac-Toe
    """
    def __init__(self, master):
        """
        Create the game of Tic-Tac-Toe

        Parameters:
        master (tk.Tk): Main window
        """
        self._master = master
        self._master.title("Tic Tac Toe")
        self._master.geometry("500x300")
        self._model = Model(self)
        self._view = View(self._master,self._model)
        
        
        # File menu
        menubar = tk.Menu(self._master)
        # tell master what it's menu is
        self._master.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="Settings", menu=filemenu)
        #What I want in the file menu
        filemenu.add_command(label="New Game", command=self.new_file)
        filemenu.add_command(label="Load Game", command=self.open_file)
        filemenu.add_command(label="Save Game", command=self.save_file)
        self._filename = None

        #Create the Design
        self._view.highlight_player()
        self._view.square_update()

    def redraw(self):
        """
        Updates the game when a round is over
        """
        self._view.square_update()
        self._view.refresh_score()

    def highlight(self,index):
        """
        Highlights the winning boxes (3 boxes)

        Parameters:
        index (List): A list containing the number (index) of the boxes that should be highlighted
        """
        for i in index:
            self._view.get_square()[i-1].highlight()
        
    def new_file(self):
        """
        Reinitialises the game (score 0-0)
        """
        
        if not self._model.get_turn():
            self._model.set_turn()
            
        self._view.highlight_player()
        self._model.set_score(0,0)
        self._model.refresh_data()
        self._view.square_update()
        self._view.refresh_score()
    
    def save_file(self):
        """
        Saves the game in an external file 
        """
        
        if self._filename is None:
            filename = filedialog.asksaveasfilename()
            if filename:
                self._filename = filename
        if self._filename:
            self._master.title(self._filename)
            fd = open(self._filename, 'w')
            #Save the score on the external file
            #note: this file could be opened to reload the game
            fd.write(str(self._model.get_score()[0]) +" "+str(self._model.get_score()[0]))
            fd.close()

    def open_file(self):
        """
        Loads a previous game and enables to continue playing
        """
        filename = filedialog.askopenfilename()
        if filename:
            score = []
            fd = fd = open(filename, "r")
            for line in fd:
                if line:
                     for char in line.split():
                         score.append(int(char))
            self._model.set_score(score[0],score[1]) #Load the score 
            if not self._model.get_turn():
                self._model.set_turn()

            #Update the game
            self._view.highlight_player()
            self._model.refresh_data()
            self._view.square_update()
            self._view.refresh_score()
            
                   
class View(tk.Grid):
    """
    The Tic-Tac-Toe interface
    """
    def __init__(self, master, model):
        """
        Create the Tic-Tac-Toe interface

        Parameters:
        master (tk.Tk): Main window
        model (Model): Model of the game (backend)
        """
        self._master = master
        self._model = model
        self._title=tk.Label(self._master,text="Tic-tac-toe Game",font='Arial 20 bold',fg = 'red')
        self._title.grid(row=0,column=0)
        self._score_label = tk.Label(self._master, text="Score: {} - {}".format(self._model.get_score()[0],self._model.get_score()[1]),font='Arial 15 bold')
        self._score_label.grid(row=3, column =0)

    def refresh_score(self):
        """
        Updates the score of the game
        """
        self._score_label = tk.Label(self._master, text="Score: {} - {}".format(self._model.get_score()[0],self._model.get_score()[1]),font='Arial 15 bold')
        self._score_label.grid(row=3, column =0)

    def square_update(self):
        """
        Reinitialises the grid
        """
        self._square=[]
        self._square_1 = Square(self._master, 1, 1," ",self._model,self,1)
        self._square_2 = Square(self._master, 2, 1," ",self._model,self,2)
        self._square_3 = Square(self._master, 3, 1," ",self._model,self,3)
        self._square_4 = Square(self._master, 1, 2," ",self._model,self,4)
        self._square_5 = Square(self._master, 2, 2," ",self._model,self,5)
        self._square_6 = Square(self._master, 3, 2," ",self._model,self,6)
        self._square_7 = Square(self._master, 1, 3," ",self._model,self,7)
        self._square_8 = Square(self._master, 2, 3," ",self._model,self,8)
        self._square_9 = Square(self._master, 3, 3," ",self._model,self,9)
        self._square = [self._square_1,self._square_2,self._square_3,self._square_4,self._square_5,
                        self._square_6,self._square_7,self._square_8,self._square_9]

    def get_square(self):
        """
        Returns a list of the 9 "boxes (data)" of the Tic-Tac-Toe Grid

        Returns:
        List: List of the 9 boxes of the Tic-Tac-Toe Grid
        """
        return self._square
    
    def highlight_player(self):
        """
        Highlights the player who has to play
        """
        if self._model.get_turn():
            player_1=tk.Label(self._master,text="Player 1: X",font='Arial 15 bold',bg="green")
            player_1.grid(row=1,column=0)
            player_2=tk.Label(self._master,text="Player 2: O",font='Arial 15 bold')
            player_2.grid(row=2,column=0)
        else:
            player_1=tk.Label(self._master,text="Player 1: X",font='Arial 15 bold')
            player_1.grid(row=1,column=0)
            player_2=tk.Label(self._master,text="Player 2: O",font='Arial 15 bold',bg="green")
            player_2.grid(row=2,column=0)
      
class Model():
    """
    The model of the Tic-Tac-Toe Grid
    """
    def __init__(self,master):
        """
        Create a model

        Parameters:
        master (Game): The Tic-Tac-Toe game
        """
        self._master = master
        self._turn = True
        self._counter = 0
        self._score = [0,0]
        self._data = [0,0,0,0,0,0,0,0,0,0]
        
    def refresh_data(self):
        """
        Reinitialises the data
        """
        self._data = [0,0,0,0,0,0,0,0,0,0] #empty boxes
        self._counter = 0 
        
    def set_score(self, score1, score2):
        """
        Changes the score of the game

        Parameters:
        score1 (int): Score of the first player
        score2 (int): Score of the second player
        """
        self._score[0]=score1
        self._score[1]=score2
        
    def get_score(self):
        """
        Returns the score of the game

        Returns:
        List: A List containing the score of the first player (int) and the score of the second player (int)
        """
        return self._score

    def set_data(self, index, text):
        """
        Changes the model to take into account in wich box a player decided to play

        Parameters:
        index (int): the box number where an "X" or an "O" has been written
        text (str): The text that was written on the box (either "X" or "O")
        """
        self._data[index] = text

    def score_update(self,text):
        """
        Updates the score at the end of a game

        Parameters:
        text (str): the player who won ("X" means player 1 and "O" means player2)
        """
        if text == "X":
            self._score[0] += 1
        elif text == "O":
            self._score[1] += 1

    def set_turn(self):
        """
        Defines which player has to play
        """
        self._turn = not self._turn

    def get_turn(self):
        """
        Returns the player which has to play

        Returns:
        bool: True if player1 has to play and False if player2 has to play
        """
        return self._turn

    def check(self):
        """
        Checks if someone has won the game or if it is a tied game
        """
        index = []
        self._counter += 1

        #Checks all possible combinations to win
        if (self._data[1] == self._data[2]) and (self._data[1]== self._data[3]) and (self._data[1] != 0):
            index = [1, 2, 3]
            self.win(self._data[1],index)
     

        elif (self._data[4] == self._data[5]) and (self._data[4]== self._data[6]) and (self._data[4] != 0):
            index = [4, 5, 6]
            self.win(self._data[4],index)
   
            
        elif (self._data[7] == self._data[8]) and (self._data[8]== self._data[9]) and (self._data[7] != 0):
            index = [7, 8, 9]
            self.win(self._data[7],index)
    
            
        elif (self._data[1] == self._data[4]) and (self._data[1]== self._data[7]) and (self._data[1] != 0):
            index = [1, 4, 7]
            self.win(self._data[1],index)

            
        elif (self._data[2] == self._data[5]) and (self._data[2]== self._data[8]) and (self._data[2] != 0):
            index = [2, 5, 8]
            self.win(self._data[2],index)
            
        elif (self._data[3] == self._data[6]) and (self._data[3]== self._data[9]) and (self._data[3] != 0):
            index = [3, 6, 9]
            self.win(self._data[3],index)
    
            
        elif (self._data[1] == self._data[5]) and (self._data[1]== self._data[9]) and (self._data[1] != 0):
            index = [1, 5, 9]
            self.win(self._data[1],index)
            
            
        elif (self._data[3] == self._data[5]) and (self._data[3]== self._data[7]) and (self._data[3] != 0):
            index = [3, 5, 7]
            self.win(self._data[3],index)
  

        elif self._counter == 9: #Check if it is a tied game
            messagebox.showinfo("Match Tied !", "Try again")
                
            self._counter = 0
            self._master.redraw()
            self.refresh_data()
            
    def win(self, text,index):
        """
        Outputs a message to show the winner

        Parameters:
        text (str): player who won ("X" corresponds to player1 and "O" to player2)
        index (list): list containing the number of the 3 boxes containing the same text
        """
        self._master.highlight(index)
        if text == "X":
            message = "Player 1 wins"
            
        elif text == "O":
            message = "Player 2 wins"
        
        #Reinitialise boxes and update score
        messagebox.showinfo("Game completed",message)
        self.score_update(text)
        self._counter = 0
        self.refresh_data()
        self._master.redraw()
        
class Square(tk.Button):
    """
    Create a box (button) in the Grid
    """
    def __init__(self, master, row, column, text,model,view,number):
        """
        Create a box

        Parameters:
        master (tk.Tk): Main window
        row (int): : the row number of the button
        column (int): the column number of the button
        text (str): the text of the button
        model (Model): The Model of the game
        view (View): The grid containing the button
        number (int): the box number
        """
        self._number = number
        self._master = master
        self._row = row
        self._column = column
        self._model = model
        self._view = view
        self._text = " "
        self._btn = tk.Button(self._master, text = self._text,bg= "darkviolet",fg="Black",width=4,font='Arial 22 bold', command = self.press)
        self._btn.grid(column = self._column, row = self._row,sticky = tk.W)

    def press(self):
        """
        Function linked to the button
        """
        if self._text == " " and self._model.get_turn(): #player 1 presses the button 
            self._btn["text"] = "X" #Updates text on the button
            self._text = "X"
            
            #update information:
            self._model.set_data(self._number,self._text)
            self._model.check()
            self._model.set_turn()
            self._view.highlight_player()
            
        elif self._text == " " and (not self._model.get_turn()): #player 2 presses the button
            self._btn["text"] = "O" #Updates text on the button
            self._text = "O"
            
            #update information:
            self._model.set_data(self._number,self._text)
            self._model.check()
            self._model.set_turn()
            self._view.highlight_player()

    def highlight(self):
        """
        Highlights a square in red
        Used when a player has won a round
        """
        self._btn = tk.Button(self._master, text = self._text,bg= "red",fg="Black",width=4,font='Arial 22 bold', command = self.press)
        self._btn.grid(column = self._column, row = self._row,sticky = tk.W)

# Data
#Top label
top_label_title = """Important"""
top_label_text = """Individual assessment items must be solely your own work. While students are encouraged to have high-level conversations about the problems they are
trying to solve, you must not look at another student's code or copy from it. The university uses sophisticated anti-collusion measures to automatically
detect similarity between assignment submissions."""

#quick questions big label
quick_question_title = 'Quick Questions'
quick_question_text = '<2 mins with a tutor'
quick_question_bg = "lightgreen"
quick_question_fg = 'darkgreen'

#long questions big label
long_question_title = 'Long Questions'
long_question_text = '>2 mins with a tutor'
long_question_bg = "lightblue"
long_question_fg = 'darkblue'
        
# Text for examples
quick_example_text = """ Some examples of quick questions:

    \u2022 Syntax errors
    
    \u2022 Interpreting error output
    
    \u2022 Assignment/MyPyTutor interpretations
    
    \u2022 MyPyTutor submission issues
    """
long_example_text = """Some examples of long questions:

    \u2022 Open ended questions
    
    \u2022 How to start a problem
    
    \u2022 How to improve code
    
    \u2022 Debugging
    
    \u2022 Assignment help
    """
#Main Buttons text
quick_button_text = """Request Quick Help"""

long_button_text = """Request Long Help"""
            
root = tk.Tk()
app = App(root)
root.mainloop()
