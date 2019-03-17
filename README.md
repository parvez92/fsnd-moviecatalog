# Project Description(Movie Catalog)
This project provides a list of movies within a variety of genres as well as provide a user registration and authentication system. Registered users have the ability to Add, Edit and delete the movies they have added.

Used Technologies : Flask, SQLAlchemy, Google and Facebook Authentication, Milligram for CSS

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Content of the Project](#content)
- [Supporting Materials](#supporting-materials)

## Installallation
The project requires python 3,Flask and SQLAlchemy.For this project all these are packaged in the Vagrant file available in the vagrant folder of the project and the file can be run on Virtual box.

### Install VirtualBox

VirtualBox is the software that actually runs the virtual machine. [You can download it from virtualbox.org, here.](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) Install the _platform package_ for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

Currently (October 2017), the supported version of VirtualBox to install is version 5.1. Newer versions do not work with the current release of Vagrant.

**Ubuntu users:** If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.

### Install Vagrant

Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. [Download it from vagrantup.com.](https://www.vagrantup.com/downloads.html) Install the version for your operating system.

**Windows users:** The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

![vagrant --version](https://d17h27t6h515a5.cloudfront.net/topher/2016/December/584881ee_screen-shot-2016-12-07-at-13.40.43/screen-shot-2016-12-07-at-13.40.43.png)

_If Vagrant is successfully installed, you will be able to run_ `vagrant --version`
_in your terminal to see the version number._
_The shell prompt in your terminal may differ. Here, the_ `$` _sign is the shell prompt._

### More Details about Virtual box and Vagrant Setup can be found here.
[VM](https://github.com/udacity/fullstack-nanodegree-vm/blob/master/README.md)


## How to Run
1. After the Virtual Machine set up is done move to vagrant folder of this project and run `vagrant up` to start the Virtual Machine.
2. For loggin into the newly setup Virtual Machine run the command  `vagrant ssh` .
3. Once logged into the Virtual Machine use `cd /vagrant/moviecatalog/` this moves you to the directory where application script resides.
4. For Starting the application run the command `python movieCatalog.py`.
5. This makes the application available on your local machine at port 5000.
6. Use any browser and access the application by typing the address `http://localhost:5000/`
7. The application has read only view of catalog of movies for the users who are not authenticated and movies already available can only    be edited or deleted by the users who created them.
8. For Logging into the application use the login button available at top right hand corner.    

## Content of the Project

#### : 
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