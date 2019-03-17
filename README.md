# Project Description(Movie Catalog)
This project provides a list of movies within a variety of genres as well as provide a user registration and authentication system. Registered users have the ability to Add, Edit and delete the movies they have added.

Used Technologies : Flask, SQLAlchemy, Google and Facebook Authentication, Milligram for CSS

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Supporting Materials](#supporting-materials)

## Installallation
The project requires python 3,Flask and SQLAlchemy.For this project all these are packaged in the Vagrant file available and the file can be run on Virtual box.

The details about installation and use of Vagrant and Virtual box can be found be here.
[VM](https://github.com/udacity/fullstack-nanodegree-vm/blob/master/README.md)


### Creating Views
The below Views have to be created in the **News** Database after connecting to DB using `psql news`.


#### Article_Views_Count view:
The following view is created to fetch how many times each Article was successfully viewed and order 
the _Articles_ in descending order.

1. This view uses the **slug** column in _Articles_ table to join the _Log_ and _Articles_ tables to find out number of times each Article was successfully viewed.
2. CONCAT function is performed on the **slug** column to find the URI **path** of the Article from _Log_ table.  

```

create view Article_Views_Count as
	select articles.author,articles.title,result.count 
	 from articles join
		(select res.slug as article,count(log.path) as count from log,(select distinct(slug) from articles) as res
	 where path in (CONCAT('/article/',CAST(slug as text))) group by res.slug order by count desc
		)as result
    on articles.slug=result.article order by count desc;

```
#### Author_Views_Count
The following view is created to fetch how many views each Author has received.

```
create view Author_Views_Count as
  select author,sum(count) as views from Article_Views_Count
  group by author
  order by views desc;
```

#### Per Day Success_Error_Count view: 
The follwing view is created to fetch the Success and Error Count data for a particular day from the _Log_ table.

1. The below view groups the data based on the **day** and **status** columns in **News** Database.
2. It uses the  _postgresql_ windows function on the above grouped data to calculate the percentage contribution of a particular Status code towards the rows logged in a day.

```
create view Success_Error_Count as 
	select status,date_trunc('day',time)::date as 
		day,count(status),trunc((100 * (count(status)/(sum(count(status)) over (partition by date_trunc('day',time)::date)))),3) 
		as percent from log 
	where status is not null group by status,date_trunc('day',time)::date;

```
## Running the Program
Copy the files in any of the directories and run the following command after changing to the direcory in which the python script has been copied.
 ```python logAnalysis.py```

## Code Description

The program calls a total of 4 Functions from MAIN for answering our 3 questions mentioned at the top.

1. **get_queryResults**: 
     This function takes a string(query) as an argument and connects to the Database,
     and performs the specified query and returns the result set of the query.
2. **get_top_Articles**:
     This function takes no arguments and prints the names and the number of views the top 3 Articles of the **News** Database.

     * **Query Used for fetching above data**: 
     ```
     select title,count from Article_Views_Count limit 3

     ```
3. **get_top_Authors**:
     This function gets the TOP Authors from **News** Database.

     * **Query Used for fetching above data**: This joins _Author_Views_Count_ view created above with _Authors_ table using the Authors unique ID to fetch the desired data.

     ```
     select authors.name,AVC.views from authors,
               Author_Views_Count AVC
               where authors.id=AVC.author
     ```
4. **get_error_Prone_days**
     Returns the days where news system received more than 1% Errors.

      * **Query Used for fetching above data**: The below query filters out only the Error status data from the data fetched by Success_Error_Count view.

     ```

     select to_char(day,'Mon DD,YYYY') as day,concat(percent,'%')
              as Error_Percent from (select * from Success_Error_Count) as qur
              where status not like '2%' and percent>1.000
     ```
## Results
A sample for the results of the script is available in 'Results.txt' file.