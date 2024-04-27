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
# SQLBooks = "SELECT product_id, product_title, star_rating, review_headline, review_body FROM amazon_reviews_multilingual_US_v1_00 WHERE product_category = 'Books'"

# Query SQL to get the categories
# SQLCategories = "SELECT DISTINCT product_category FROM amazon_reviews_multilingual_US_v1_00 GROUP BY product_category"
# dfCategories = con.sql(SQLCategories)
# numpyCategories = dfCategories.fetchnumpy()
# print(numpyCategories)

# Columns I want to get: product_title product_category, review_headline, review_body
# Now I want to get all the above columns together into one dataframe from the Books by calling an SQL query
# categoryName = 'Books'
# SQLQuery = "SELECT product_title, product_category, review_body FROM amazon_reviews_multilingual_US_v1_00 WHERE product_category = " + categoryName + " AND LENGTH(review_body) > 5000;"
# dfCategory = con.sql(SQLQuery)
# numpyBooks = dfBooks.fetchnumpy()
# Get a list of the review_body column from dfBooks
# categoryReviewsList = dfCategory["review_body"].fetchnumpy()
# print(type(categoryReviewsList))
# dfBookReviews = dfBooks["review_body"].to_list()

# SQLBooksTotal = "SELECT review_body FROM amazon_reviews_multilingual_US_v1_00 WHERE product_category = 'Books'"
# dfTotalBooks = con.sql(SQLBooksTotal)
# totalBooksList = dfTotalBooks["review_body"].fetchnumpy()
# print("Size of total book amount is ",len(totalBooksList["review_body"]))
# Total amount of book reviews is 838,801!

#Get the column names
# columnNames = dfCategory.columns
# print(columnNames)
# print(dfBooks)

# Now I want to get all the above columns together into one dataframe by calling an SQL query
# SQLTotal = "SELECT customer_id, review_id, product_id, product_category, star_rating, helpful_votes, total_votes, vine FROM amazon_reviews_multilingual_US_v1_00"
# dfTotal = con.sql(SQLTotal)
# numpyTotal = dfTotal.fetchnumpy()
# print(dfTotal) # Print the results

# We now have all the columns we need in the numpy arrays

# To test to see how we can use the numpyBooks array to get the review_body so we can use it with the NER model, we'll test for the first review_body
# First, we need to get review_body from the first row
# strReviewBody = bookReviewsList["review_body"][0]
# print(strReviewBody)
# nlpBody = nlp(strReviewBody)
# print(nlpBody)
categoryReviewsList = 2
def queryTime(categoryName):
    SQLQuery = "SELECT product_title, product_category, review_body FROM amazon_reviews_multilingual_US_v1_00 WHERE product_category = '" + categoryName + "' AND LENGTH(review_body) > 1000;"
    categoryReviewsList = con.sql(SQLQuery)
    count = len(categoryReviewsList["review_body"])
    print("There are", count, "", categoryName, " total reviews to work with")
    categoryReviewsList = categoryReviewsList["review_body"].fetchnumpy()
    # The goal is to get the number of times people are mentioned in the review_body
    personCount = 0
    # For each review_body in the numpy product category array, get the number of times people are mentioned from the NER model  
    for i in range(count):
        strReviewBody = categoryReviewsList["review_body"][i]
        nlpBody = nlp(strReviewBody)
        # If "I-PER" exists as one of the values in the dictionary, add to the count and continue
        for j in nlpBody:
            if j["entity"] == "I-PER":
                personCount += 1
                break

    return personCount

print("Time to work with the Video Games!")
personscounted = queryTime("Video Games")
print("The number of times people are mentioned in video game reviews: ", personscounted)
# print("Time to work with videos!")
# personscounted = queryTime("Video")
# print("The number of times people are mentioned in video game reviews: ", personscounted)
# fileT = open("text.txt", "w")
# result = "The number of times people are mentioned in movie and TV show reviews: " + str(personscounted)
# print(result)
# fileT.write(result)
# fileT.close()
print("When working with 1717 video game reviews, the number of times people are mentioned in them are 56") # Length > 1000 characters
# print("When working with 3915 video game reviews, the number of times people are mentioned in them are 91") # Length > 500 characters
print("When working with 11851 movie and TV show reviews, the number of times people are mentioned in them are 10078")
print("When working with 9961 book reviews, the number of times people are mentioned in them are 7617")
