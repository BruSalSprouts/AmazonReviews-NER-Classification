import duckdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
con = duckdb.connect("amazon_reviews.duckdb")

# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
nlp = pipeline("ner", model=model, tokenizer=tokenizer)

# nlpTest = nlp("Hugging Face Inc. is a company based in New York City. Its headquarters are in DUMBO, therefore very close to the Manhattan Bridge.")
# print(type(nlpTest[0]))
# For each dictionary in the list nlpTest, print the keys
# for i in nlpTest:
#     print(i.keys())

# Show only the product title and the number of reviews for each product
# from the amazon_reviews table
# and store the results into df

columnNames = ["marketplace", "customer_id", "review_id", "product_id", "product_parent", "product_title", 
               "product_category", "star_rating", "helpful_votes", "total_votes", "vine", "verified_purchase", "review_headline", "review_body", "review_date"]

SQLTitleGet = "USE amazon_reviews"

# Query SQL to get the entire dataset
SQLTotal = "SELECT * FROM amazon_reviews_multilingual_US_v1_00 GROUP BY product_title"

# Query SQL to get the product_id, product_title, product_category, star_rating, review_headline, review_body
SQLBooks = "SELECT product_id, product_title, star_rating, review_headline, review_body FROM amazon_reviews_multilingual_US_v1_00 WHERE product_category = 'Books'"

# Query SQL to get the categories
# SQLCategories = "SELECT DISTINCT product_category FROM amazon_reviews_multilingual_US_v1_00 GROUP BY product_category"
# dfCategories = con.sql(SQLCategories)
# numpyCategories = dfCategories.fetchnumpy()
# print(numpyCategories)

# Query SQL to get everything from the Books category
# SQLBooksFull = "SELECT * FROM amazon_reviews_multilingual_US_v1_00 WHERE product_category = 'Books'"
# dfBooks = con.sql(SQLBooks)
# numpyBooks = dfBooks.fetchnumpy()



#Get the column names
# columnNames = dfBooks.columns
# print(columnNames)
# print(dfBooks)
# Columns I want to get: product_title product_category, review_headline, review_body
# Now I want to get all the above columns together into one dataframe from the Books by calling an SQL query
SQLTotalBooks = "SELECT product_title, product_category, review_headline, review_body FROM amazon_reviews_multilingual_US_v1_00 WHERE product_category = " + "Books"
dfBooks = con.sql(SQLTotalBooks)
numpyBooks = dfBooks.fetchnumpy()

# Now I want to get the above columns together into one dataframe from the movies_and_TV by calling an SQL query
SQLTotalMovies = "SELECT product_title, product_category, review_headline, review_body FROM amazon_reviews_multilingual_US_v1_00 WHERE product_category = " + "Movies_and_TV"
dfMovies = con.sql(SQLTotalMovies)
numpyMovies = dfMovies.fetchnumpy()

# Now I want to get the above columns together into one dataframe from the Video games by calling an SQL query
SQLTotalVideoGames = "SELECT product_title, product_category, review_headline, review_body FROM amazon_reviews_multilingual_US_v1_00 WHERE product_category = " + "Video Games"
dfVideoGames = con.sql(SQLTotalVideoGames)
numpyVideoGames = dfVideoGames.fetchnumpy()

# print(dfTotal) # Print the results

# We now have all the columns we need in the numpy arrays

# To test to see how we can use the numpyBooks array to get the review_body so we can use it with the NER model, we'll test for the first review_body
# # First, we need to get review_body from the first row
# strReviewBody = numpyBooks["review_body"][0]
# print(strReviewBody)
# nlpBody = nlp(strReviewBody)
# print(nlpBody)

print("Time to work with the books!")
print("Number of reviews in the Books category: ", len(numpyBooks["review_body"]))
def personCounting():
    # The goal is to get the number of times people, organizations, or locations are mentioned in the review_body
    personCount = 0
    # For each review_body in the numpyBooks array, get the number of times people, organizations, or locations are mentioned from the NER model  
    for i in range(len(numpyBooks["review_body"])):
        strReviewBody = numpyBooks["review_body"][i]
        nlpBody = nlp(strReviewBody)
        for j in nlpBody:
            if j["entity"] == "I-PER":
                personCount += 1
                break
        boolPerson = False
    return personCount

def movieReview():
    print("Time to work with the movies!")
    print("Number of reviews in the Movies category: ", len(numpyMovies["review_body"]))
    # For each review_body in the numpyMovies array, get the number of times people, organizations, or locations are mentioned from the NER model
    personCount = 0
    boolPerson = False
    for i in range(len(numpyMovies["review_body"])):
        strReviewBody = numpyMovies["review_body"][i]
        nlpBody = nlp(strReviewBody)
        for j in nlpBody:
            if j["entity"] == "I-PER" and not boolPerson:
                personCount += 1
                break
        boolPerson = False
    print("Number of times people are mentioned in the movie reviews: ", personCount)

print("Time to work with the video games!")
print("Number of reviews in the Video Games category: ", len(numpyVideoGames["review_body"]))
# For each review_body in the numpyVideoGames array, get the number of times people, organizations, or locations are mentioned from the NER model
personCount = 0
boolPerson = False
for i in range(len(numpyVideoGames["review_body"])):
    strReviewBody = numpyVideoGames["review_body"][i]
    nlpBody = nlp(strReviewBody)
    for j in nlpBody:
        if j["entity"] == "I-PER" and not boolPerson:
            personCount += 1
            break
    boolPerson = False
print("Number of times people are mentioned in the video game reviews: ", personCount)
