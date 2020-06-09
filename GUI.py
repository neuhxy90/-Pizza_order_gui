# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.scrolledtext import *

class RatingFrameGUI:
    def __init__(self, parent):
        #create frame1
        self.rating_strings = ["No Rating", "Forget it", "2","3","4","Must See"]
        self.movies = ["The Hobbit", "Skyfall", "Captian America"]

        # define a dict to store the movie and ranking value
        self.movie_rank = {m:self.rating_strings[0] for m in self.movies}
        
        # set radio value
        self.v1 = StringVar()
        self.v1.set(self.rating_strings[0])    # Add default value parameter.

        # set radio value
        self.v2 = StringVar()
        self.v2.set(self.rating_strings[0])    # Add default value parameter.
        
        self.frame1 = Frame(parent, bg="chartreuse", padx=30, width = 200, height = 200)
        self.frame1.grid(row = 0, columnspan = 6)

        #rate label
        self.label2 = Label(self.frame1, text = "Please rate:", bg = "chartreuse")
        self.label2.grid(row=0, column=0, sticky = W, pady = 1)

        # moive name
        self.label3 = Label(self.frame1, text = self.movies[0], bg = "chartreuse")
        self.label3.grid(row=0, column=1, sticky = W, pady = 5)
    
        #rating radiobuttons, adding ", sticky=W" to make the radio-buttons left-alignment.
        self.rbs = []
        for i in range(len(self.rating_strings)):  
            rb = Radiobutton(self.frame1, variable = self.v1,
                        text = self.rating_strings[i],
                        value = self.rating_strings[i], 
                        command = self.update_movie_ranking,
                        bg = "chartreuse")
            rb.grid(row = i+1, column = 1, pady = 5, sticky=W)
            self.rbs.append(rb)

        #previous and next button
        Button(self.frame1, text = "Previous", command=self.previous).grid(row = 7, column = 0)
        Button(self.frame1, text = "Next", command=self.next).grid(row = 7, column = 1)


        self.bf = Frame(parent, padx=30, width = 200, height = 30)
        self.bf.grid(row = 6, columnspan = 6)

        #search label
        self.label1 = Label(self.bf, text = "Search for movies with a rating of:")
        self.label1.grid(row=1, column=0,columnspan=6, sticky = E+W, pady = 6)
        
        #bottom radiobuttons
        for i in range (len(self.rating_strings)):  
            Radiobutton(self.bf, 
                variable = self.v2,
                command=self.rank,
                text = self.rating_strings[i],
                value = self.rating_strings[i]).grid(row = 2, column = i, padx = 5 )


        self.frame2 = Frame(parent, bg="pink", padx=30, width = 200, height = 200)
        self.frame2.grid(row = 0, columnspan = 2)

        self.sum_label = Label(self.frame2, text='You have giving the following movies a rating of ', bg="pink")
        self.sum_label.grid(row=0, column=0, sticky= SE, padx=10)

        self.sum_value = Label(self.frame2, bg="pink")
        self.sum_value.grid(row=0, column=1, sticky= W, padx=10)

        self.res = ScrolledText(self.frame2, width=55, height=10, wrap='word')
        self.res.grid(row=1, columnspan=2)

        self.back_btn = Button(self.frame2, command=self.back, text='Back to Rating')
        self.back_btn.grid(row=2, column=1, sticky=E)
        self.frame2.grid_forget()

    def update_movie_ranking(self):
        rank = self.v1.get()
        moive_name = self.label3["text"]
        self.movie_rank[moive_name] = rank


    def previous(self):
        current = self.label3["text"]           # get current movie name.
        index = self.movies.index(current)      # get the poisition of current moive in the movie list.
        if index == 0: index = len(self.movies) # re-define the poisition if current movie is the first one in the movie list.
        nex = self.movies[index-1]              # get the poisition of previous movie.
        self.label3.configure(text=nex)         # change the name of current movie.
        self.v1.set(self.movie_rank[nex])       # change the ranking of current movie.


    def next(self):
        current = self.label3["text"]
        index = self.movies.index(current)
        if index == len(self.movies) -1: index = -1
        nex = self.movies[index+1]
        self.label3.configure(text=nex)
        self.v1.set(self.movie_rank[nex])
        

    def rank(self):
        self.res.delete(1.0, END)
        self.frame1.grid_forget()
        self.bf.grid_forget()
        self.frame2.grid(row = 0, columnspan = 2)
        self.bf.grid(row = 6, columnspan = 6)

        current = self.v2.get()
        # calculate the amount of movies with current ranking.
        movies = [m for m in self.movie_rank if self.movie_rank[m] == current]
        num = len(movies)
        self.sum_value.configure(text=current)
        # print(movies)
        for i,m in enumerate(movies): self.res.insert(END, '%s\n'%m)

    
    def back(self):
        self.res.delete(1.0, END)
        self.bf.grid_forget()
        self.frame2.grid_forget()
        self.frame1.grid(row = 0, columnspan = 6)
        self.bf.grid(row = 6, columnspan = 6)


#main
if __name__ == '__main__':
    root = Tk()
    buttons = RatingFrameGUI(root)
    root.title ("Movie Ratings")
    root.mainloop()