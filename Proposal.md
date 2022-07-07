# Predicting the Popularity of User Movie Reviews on Letterboxd


## Summary

Letterboxd is a popular film cataloging site launched in 2011 that has 1.5 million users as of November 2019. Letterboxd has created a community primarily centered around user opinions. Unlike IMDB, Letterboxd film pages do not contain trivia, long and detailed plot synopses, or dozens of photos from the film. The film pages are clean and uniform: there is a minimalistic summary of film details followed entirely by user reviews and user-created lists.

The layout and content of the front page further highlights Letterboxd’s user-centric focus: it is almost entirely populated by films that people you have followed have recently rated, and the top user reviews.

<img src="https://i.ibb.co/ZNsbRhn/letterboxd-front-page.png" title="Letterboxd front page" />

<div align="center">
    <i>Snapshot of the front page of Letterboxd, populated with user content</i></div>



## Aim

On Letterboxd, users have the ability to “like” any number of reviews. The top three “liked” reviews for each movie appear prominently at the top of that film’s homepage. Additionally, the most popular reviews are often featured on the front page of Letterboxd, further bolstering their visibility.

Thus, popular reviews are an integral component of the site experience. Given their importance, we aim to identify what factors determine a review’s popularity. How simple or difficult would it be to pen a top review? Given the high visibility of highly “liked” reviews, there are interesting implications for the ability to write extremely popular reviews. A person who is able to effectively write reviews is likely able to influence the consensus on a film on the site. 

While we would expect some predictable factors would determine the popularity of a review, such as the number of followers that a user has, there may be more interesting results that come of our analysis. Additional questions that we can explore include: Are long reviews or short reviews preferred by users? Do positive reviews resonate more than negative reviews? Do audiences of different genres prefer different types of reviews?

## Relevant Prior Work

It does not appear that user reviews have been studied in the way that we have set out to do in this project. Most of the data analysis projects collecting data from film sites attempt to either create a recommendation algorithm or predict the rating of films. 

For example, [this study](https://www.researchgate.net/publication/309820851_Predicting_Movie_Success_Based_on_IMDB_Data) from 2014 uses regression analysis on data collected from IMDB and RottenTomatoes in order to determine the optimal model for predicting movie success. Although they use RottenTomatoes user reviews in their analysis, the focus is on movie success, and not the reviews themselves, as with most other studies in this area.  

Our goal for this project is to examine the factors that predict success of the review itself. We are interested in learning more about the social aspects of online film sites. 

Although [this 2014 study published in an Advertising journal](https://www.tandfonline.com/doi/abs/10.1080/10641734.2018.1503113?journalCode=ujci20) examines Facebook posts, it is closer to our analysis than the previous study. The researchers set out to determine what makes a brand post engaging. Engaging content in measured in likes, comments, and shares. While the researchers studied variables such as number of words and number of characters, they also coded each brand post manually for certain qualitative measures in order to perform this study. In contrast, we will primarily be focused on measures that can be automatically extracted from the review or film data. 
 
## Dataset

Since Letterboxd has a private API, we will scrape Letterboxd for reviews using a combination of AutoScraper, Scrapy and Selenium. Since Letterboxd uses JavaScript to dynamically load the content of its pages, we are unable to use Scrapy or AutoScraper alone and must pair it with Selenium in order to access the content we want to analyze.

We will use the Letterboxd list of films, ordered from most popular to least popular, to scrape a fixed number of films for analysis. Since all film pages are set up uniformly, as shown below, we will find the XPath of each desired element, which will include basic film information and top reviews, and use the XPath to extract those elements for each film we choose to include in our analysis. 


<img src="https://i.ibb.co/Qb7pgDM/image.png" title="Letterboxd film page" />

<div align="center">
    <i> Letterboxd page for the film Tenet. All film pages follow the same layout
</i></div>


# Proposed Analysis Techniques

- **Multivariate Analysis**: Scatterplot matrix, as a data overview which frames further analysis.

- **Linear Regression**: Predicting using factors which determine review success.

- **Logistic Regression**: Used to predict number of likes on reviews using factors which determine review success.

- **Clustering**: Using K-means to develop clusters containing similar reviews, perhaps by genre, word count, positive reviews, negative reviews

- **Supervised Learning**: Through SVM we will advance our model


# Milestones

Each milestone represents 20% completion.

- **Milestone 1. Preparation**: Firstly, to develop our python based web scraping script to gather the data. This component is estimated to be completed by the **30th of September 2020**

- **Milestone 2. Clean**: Secondly, identifying and correcting null or unfinished values and dealing with irrelevant data that is obtained through our web scraping utility. This component is estimated to be completed by the **4th of October 2020**

- **Milestone 3 Explore**: Thirdly, application of our analysis techniques to find trends and statistical patterns. This component is estimated to be completed by the **11th of October 2020**

- **Milestone 4 Model**: Fourthly, the creation and scripting of models which will predict and forecast the popularity of user movie reviews and again applying analysis techniques to compare the results. This component is estimated to be completed by the **18th of October 2020**

- **Milestone 5 Interpret**: Finally, a curation of our findings and their relevance in the format of a video presentation. This component is estimated to be completed by the **25th of October 2020** and presented in week 13 to conclude our research.
