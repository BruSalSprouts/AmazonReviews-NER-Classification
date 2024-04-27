import duckdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

con = duckdb.connect("amazon_reviews.duckdb")

# Show only the product title and the number of reviews for each product
# from the amazon_reviews table
# and store the results into df

# Query SQL to get the entire dataset
# SQLTotal = "SELECT * FROM amazon_reviews_multilingual_US_v1_00 GROUP BY product_title"
# Print the results
# df = con.sql(SQLTotal)

# Whatever loads in the SQL query will be stored in the df variable
# Can do all preprocessing in SQL query. Fast and performant

# So first we need to get the columns we want to use
# Let's start with the customer_ID 
sqlQueryCustomerID = "SELECT customer_id FROM amazon_reviews_multilingual_US_v1_00"
dfCustomerID = con.sql(sqlQueryCustomerID)
numpyCustomerID = dfCustomerID.fetchnumpy()
# print(dfCustomerID) # Print the results

# Next, let's get the review_id
sqlQueryReviewID = "SELECT review_id FROM amazon_reviews_multilingual_US_v1_00"
dfReviewID = con.sql(sqlQueryReviewID)
numpyReviewID = dfReviewID.fetchnumpy()
# print(dfReviewID) # Print the results

# Next, let's get the product_id
sqlQueryProductID = "SELECT product_id FROM amazon_reviews_multilingual_US_v1_00"
dfProductID = con.sql(sqlQueryProductID)
numpyProductID = dfProductID.fetchnumpy()
# print(dfProductID) # Print the results

# Next, let's get the product_category
sqlQueryProductCategory = "SELECT product_category FROM amazon_reviews_multilingual_US_v1_00"
dfProductCategory = con.sql(sqlQueryProductCategory)
numpyProductCategory = dfProductCategory.fetchnumpy()
# print(dfProductCategory) # Print the results

# Next, let's get the star_rating
sqlQueryStarRating = "SELECT star_rating FROM amazon_reviews_multilingual_US_v1_00"
dfStarRating = con.sql(sqlQueryStarRating)
numpyStarRating = dfStarRating.fetchnumpy()
# print(dfStarRating) # Print the results

# Next let's get the helpful_votes
sqlQueryHelpfulVotes = "SELECT helpful_votes FROM amazon_reviews_multilingual_US_v1_00"
dfHelpfulVotes = con.sql(sqlQueryHelpfulVotes)
# I want to fill in the missing values in the helpful_votes column with 0
# dfHelpfulVotes.fillna(0)
numpyHelpfulVotes = dfHelpfulVotes.fetchnumpy()
# print(dfHelpfulVotes) # Print the results

# Next let's get the total_votes
sqlQueryTotalVotes = "SELECT total_votes FROM amazon_reviews_multilingual_US_v1_00"
dfTotalVotes = con.sql(sqlQueryTotalVotes)
# I want to fill in the missing values in the total_votes column with 0
# dfTotalVotes.fillna(0)
numpyTotalVotes = dfTotalVotes.fetchnumpy()
# print(dfTotalVotes) # Print the results

# Next let's get the vine
sqlQueryVine = "SELECT vine FROM amazon_reviews_multilingual_US_v1_00"
dfVine = con.sql(sqlQueryVine)
# dfVine.fillna('N')
numpyVine = dfVine.fetchnumpy()
# print(dfVine) # Print the results

# Now I want to get all the above columns together into one dataframe by calling an SQL query
SQLTotal = "SELECT customer_id, review_id, product_id, product_category, star_rating, helpful_votes, total_votes, vine FROM amazon_reviews_multilingual_US_v1_00"
dfTotal = con.sql(SQLTotal)
numpyTotal = dfTotal.fetchnumpy()
# print(dfTotal) # Print the results

# At this point, the preprocessing is done in SQL query
# From here, can do further processing in Python 


# print(type(numpyTotal))
# print(numpyTotal.keys())
# print(type(numpyTotal['customer_id']))

# # Normalize the star_rating numpy array with min-max normalization
# npMax = np.max(numpyTotal['star_rating'])
# npMin = np.min(numpyTotal['star_rating'])
# numpyTotal["star_rating"] = (numpyTotal["star_rating"] - npMin) / npMax

# # Normalize the helpful_votes numpy array with min-max normalization
# npMax = np.max(numpyTotal['helpful_votes'])
# npMin = np.min(numpyTotal['helpful_votes'])
# numpyTotal["helpful_votes"] = (numpyTotal["helpful_votes"] - npMin) / npMax
# print(numpyTotal["helpful_votes"])

# # Normalize the total_votes numpy array with min-max normalization
# npMax = np.max(numpyTotal['total_votes'])
# npMin = np.min(numpyTotal['total_votes'])
# numpyTotal["total_votes"] = (numpyTotal["total_votes"] - npMin) / npMax
# print(numpyTotal["total_votes"])

# Here we've done the processing in in Python
# Now it's time to plot the data into scatter plots
# plt.scatter(numpyTotal["total_votes"], numpyTotal["helpful_votes"])
# plt.xlabel('Total Votes')
# plt.ylabel('Helpful Votes')
# plt.title('Total Votes vs Helpful Votes')
# plt.show()

# So the above code is for generalized total votes and helpful votes.
# Now we need to get the total votes and helpful votes for each category
# We gotta query the SQL database for each category and store the results in a dataframe
# Then we can convert the dataframe into a numpy array, where we can do the processing
# (which is min-max normalization in this case) and then plot the data


print("=========================================")
sqlCategories = "SELECT DISTINCT product_category FROM amazon_reviews_multilingual_US_v1_00"
dfCategories = con.sql(sqlCategories)
numpyCategories = dfCategories.fetchnumpy()

# Books, Sports, Wireless, Apparel, Software, Watches, Video DVD, Office Products, Electronics, Video Games, Video,
# Mobile Electronics, PC, Outdoors, Music, Health & Personal Care, Home Entertainment, Beauty, Pet Products,
# Personal_Care_Appliances, Mobile_Apps, Camera, Luggage, Home Improvement, Tools, Lawn and Garden
# Furniture, Grocery, Digital_Ebook_Purchase, Digital_Video_Download, Digital_Music_Purchase,
# Musical Instruments, Automotive, Shoes, Baby, Kitchen, Home, Toys

# print(dfCategories)
# print(numpyCategories)

# Open CSV file in which normalized values will be stored

# Takes in a string (category), queries the SQL database for the category, normalizes the data, and plots the data
def categorySQLToPlot(category):
    sqlVotes = "SELECT total_votes, helpful_votes FROM amazon_reviews_multilingual_US_v1_00 WHERE product_category = " + category
    dfVotes = con.sql(sqlVotes)
    numpyVotes = dfVotes.fetchnumpy() # Convert the dataframe into a numpy array
    print("The total number of items in the category " + category + " is " + str(len(numpyVotes['total_votes'])))
    # Helpful votes
    npMax = np.max(numpyVotes['helpful_votes'])
    npMin = np.min(numpyVotes['helpful_votes'])
    npMaxMin = npMax - npMin
    numpyVotes["helpful_votes"] = (numpyVotes["helpful_votes"] - npMin) / npMaxMin
    # Total votes
    npMax = np.max(numpyVotes['total_votes'])
    npMin = np.min(numpyVotes['total_votes'])
    npMaxMin = npMax - npMin
    numpyVotes["total_votes"] = (numpyVotes["total_votes"] - npMin) / npMaxMin

    # Store the normalized values in a csv file
    

    # Scatter plot
    # plt.scatter(numpyVotes["total_votes"], numpyVotes["helpful_votes"])
    # plt.xlabel('Total Votes')
    # plt.ylabel('Helpful Votes')
    # plt.title(category + ' - Total Votes vs Helpful Votes')
    # plt.show()
    # plotImage = plt.savefig('images/' + category + '.png')
    # Clear the plot
    plt.clf()
    
print("Printing the categories in the plot")
# # Now we need to get the total votes and helpful votes for each category
# #We'll make a for loop that goes through each category and calls the function
for i in range(len(numpyCategories['product_category'])):
    categorySQLToPlot("'" + numpyCategories['product_category'][i] + "'")
print("Done printing the categories in the plot")

# So the above code is all the categories that we have in the dataset
# Now we need to make general functions that can take in the category as a parameter
# and then do the rest of the processing and plotting



# print(df)
