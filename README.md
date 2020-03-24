# Exploratory Yelp Data Analysis -- STA 220 Final Project

## Group: Yiming Wu, Zhuowei Chen, Chenghan Sun

## Project Overview and Motivations

### Part I: Motivation of this data science project <a class="anchor" id="sub1"></a>

As we expected, in this era of information exposion, people are keen to use data to reveal underlying patterns and behaviors from macro perspectives. Thus, no surprise that there already existed numerous data science projects which broadly focused on commercial datasets. From another aspect, with the rapid development and implementation of Machine Learning algorithms, majority of these projects heavily focused on data forecasting and general insights, such as conducting sentiment analysis on tweets. However, several questions remained to be answer:

- What if we don't have available datasets? 
    - How should we deal with massive and mixed raw data?
- As data analysts / scientists, how should we explain and deliver the data insights to non-experts?
- Could we optimize the data pipeline and analysis?

These above questions need to be carefully considered before implementation of any Machine Learning algorithms, and play an important role in data science field. Thus, we want to highlight potential solutions and benchmark the above questions in this project:

- Implement web crawler technologies to collect raw dataset
    - Perfrom data cleaning and feature engineering on the crawled dataset
- Perfrom exploratory data analysis and gain data insights using graphical visualization tools
- Create automatic data pipeline through the whole project

In this project, we choose to perform above strategies on Yelp (https://www.yelp.com/) for benchmarking purpose. Yelp is a great data repository which thrives on the numerous descriptive features that are provided by owners of local restaurants. It is of considerable value to analyze Yelp data and find out whether they help in directing the performance of restaurant or whether restaurant performance is indeed dictated by other factors. given the context: 

- **This project is heavily focused on:**
    - 1. Project organization, writeup readability, and overall conclusions
        - This part will be separately explained in the Part II: Usage and organization of folder structure.
    - 2. Code quality, readability, and efficiency
        - We grouped code functionalities by different classes. See details in Part II: Usage and organization of folder structure.
    - 3. Scientific programming and custom algorithms
        - We design and implement many unique algorithms for efficient data processing, details in Folder: Build_Craler and Codebase.
    - 4. Data munging
        - We export data from sql server to DataFrame, and perfromed extensive data munging to perfrom effcient analysis.
    - 5. Data visualization
        - We perfromed data visualization extensively on all features we crawled from Yelp, and made comments on insights in the graphical information.
    - 6. Data extraction
        - We highlight the spirit of web techlogies, especially on wed crawler. We built our own unique code (see Build_Crawler folder) to collect data. In addition, this module could be easily modified to crawl even more data from Yelp, or apply to other websites based on similar principle.
    - 7. Data storage and big data
        - We deigned the data pipeline to store all data into relational database and interact through SQL queries.
    - 8. Statistics and machine learning
        - We provided some modeling (e.g. classification) and highlight the data insights and advice for future works.
        

### Part II: Usage and organization of folder structure <a class="anchor" id="sub2"></a>

**There are fours major folders in the submitted folder:**
- 1. Notebooks
    - Main_notebook.ipynb:
        - Contains all project introductions, strcutures, explanations, observations and comments, visualizations, modelings and summaries. Please refer this notebook as principal line of the project.
        
        
- 2. Build_Crawler:

    - We built a seperate scrapy-based Yelp web crawling module into this folder. As a individual module, this means it could be easily modified to crawl even more user-specified data from Yelp, or apply this crawling method to other websites based on similar principle. The main class lives in Build_Crawler/Yelp/spiders/YelpSpider.py, and other help classes and pipelines were also built in Build_Crawler/Yelp. We automate the data collection process by implementing SQL queries. All data were automatically stored into local SQL server.  


- 3. Database:
    - We have four sub-folders:
        - yelp_dbs:
            - `yelp_db_1_6.sql` contains information of the following cities:  
            |-----------------------|  
            | Tables_in_yelp_db_1_6 |  
            |-----------------------|  
            | yelp_fresno           |  
            | yelp_los_angeles      |  
            | yelp_sacramento       |  
            | yelp_san_diego        |  
            | yelp_san_francisco    |  
            | yelp_san_jose         |  
            |-----------------------|    
            6 rows in set (0.00 sec) 
            - `yelp_db_7_12.sql` contains information of the following cities:  
            |------------------------|  
            | Tables_in_yelp_db_7_12 |  
            |------------------------|  
            | yelp_Anaheim           |  
            | yelp_Bakersfield       |  
            | yelp_Long_Beach        |  
            | yelp_Oakland           |  
            | yelp_Riverside         |  
            | yelp_Santa_Ana         |  
            |------------------------|   
            6 rows in set (0.00 sec)  
        - cities_csv:
            - Contains information of crawled California city list from https://en.wikipedia.org/wiki/List_of_largest_California_cities_by_population. Please refer Section I, Part I for more details. 
        - resource_csv:
            - Contains information of fipsDict downloaded from https://data.world/niccolley/us-zipcode-to-county-state. We map fips code to zip code and corresponding city information. This .csv file will be used in Geo-Spatial analysis in Section III, Part V. 
            
            
- 4. Codebase
    - There following .py file lives in this folder:
        - db_utils.py: Use for database (SQL server) connection and extract data into dataframe for analysis.
        - helper_fe.py: contained all data cleaning and feature engineering.
        - ratdist_plot.py: ratings distribution plots
        - category_plot.py: categorical plots
        - ophrs_plot.py: operation hrs plots
        - helper_ml.py: ML plots


