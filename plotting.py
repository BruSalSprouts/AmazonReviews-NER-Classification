import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# print("When working with 1717 video game reviews, the number of times people are mentioned in them are 56") # Length > 1000 characters
# print("When working with 11851 movie and TV show reviews, the number of times people are mentioned in them are 10078")
# print("When working with 9961 book reviews, the number of times people are mentioned in them are 7617")

movieNumberWorkedWith = 9961
movieNumberMentioned = 7617
movieNumberMentionedRatio = movieNumberMentioned / movieNumberWorkedWith
movieNumberNotMentioned = movieNumberWorkedWith - movieNumberMentioned
movieNumberNotMentionedRatio = 1 - movieNumberMentionedRatio

def piePlotPortions(proportionNum1, proportionNum2, categoryName):
    labels = "Characters are Mentioned", "Characters aren't mentioned"
    sizes = [85.03, 14.97]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%")
    plt.title("How many movie and TV show reviews mention characters \nVS \nHow many don't")
    plt.show()
    plt.savefig('images/videoGameNumberRatio.png')
piePlotPortions(movieNumberMentionedRatio, movieNumberNotMentionedRatio, "Movies and TV Shows")