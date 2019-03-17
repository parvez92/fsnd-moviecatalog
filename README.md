# Project Description(Movie Catalog)
This project provides a list of movies within a variety of genres as well as provide a user registration and authentication system. Registered users have the ability to Add, Edit and delete the movies they have added.

Used Technologies : Flask, SQLAlchemy, Google and Facebook Authentication, Milligram for CSS

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Capabilities of the Application](#Capabilties)
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

## Capabilities of the Application
1. For an Unauthenticated and Unregisterd user the application will serve the all the Genre and Movie details as read-only.
2. User can use the log-in option availale on top right hand corner for accessing the application.
3. An User can use either their google or facebook account to log in to the application.
4. Once log-in is completed the button shows logout.
5. An Authenticated user can only edit or delete the movies he has created.
6. Authenticated Users have the ability to add new movies to a particular genre or add new genres. 
7. Once the Genre is created the Users cannot Edit or Delete the Genre as other users may add movies to the genre and it would effect their data.
8. Flash messages would be displayed after successfull Addition or Editing or Deletion of Movies.
9. The Application is available at port:5000  


## How to Run
1. After the Virtual Machine set up is done move to vagrant folder of this project and run `vagrant up` to start the Virtual Machine.
2. For logging into the newly setup Virtual Machine run the command  `vagrant ssh` .
3. Once logged into the Virtual Machine use `cd /vagrant/moviecatalog/` this moves you to the directory where application script resides.
4. For Starting the application run the command `python movieCatalog.py`.
5. This makes the application available on your local machine at port 5000.
6. Use any browser and access the application by typing the address `http://localhost:5000/`
7. The application has read only view of catalog of movies for the users who are not authenticated and movies already available can only    be edited or deleted by the users who created them.
8. For Logging into the application use the login button available at top right hand corner.    

#### JSON ENDPOINTS:
The application serves JSON endpoints for making API calls to fetch the movie data the below URI endpoints are available for fetching data.
For accessing the API's please use `http://localhost:5000/` followed by the URI below the **int** values should be replaced with valid values for accessing the data.  

1. **URI:/moviecatalog/JSON** This URI serves all the movie Genres available. 
2. **URI:/moviecatalog/int:genre_id/JSON** This URI serves all the movies available in a particular genre. 
3. **URI:/moviecatalog/int:genre_id/movies/JSON** This URI serves all the movies available in a particular genre.
4. **URI:/moviecatalog/int:genre_id/movie/int:movie_id/JSON** This URI serves the movie description of the movie queried.

## Content of the Project

#### Vagrantfile: 
This file contains the configuration of the Virtaul Machine that should be created.

#### dataBase_Setup.py:
This file creates the database configuration required for the application.The database has three tables.
1. **UserDetails:** To hold the user details who are using the application.
2. **MovieCategory:** To hold the Genre deatails of the movies.
3. **MovieDetails:** To hold the movie details.

#### createMovieCatalogDb.py:
This file loads the intial test data into the database.


#### static and template folders:
This static and template folders hold the CSS and HTML files that would be served by the application.


#### movieCatalog.py:
The movieCatalog python script holds the code for serving the application the following the methods are available in the script.
1. **showGenres():** This method serves the catalog's home page with all the Movie and Genre details. 
2. **showGenre(genre_id):** This method serves the genre.html page with all the Movies related to a particular Genre.
3. **showMovie(genre_id, movie_id):** This method serves the movieDetails.html page with the descrption of the Movie selected and provides the creator of the movie to edit or delete the movie.
4. **addMovie():** This method serves the addMovie.html page to add a new movie to the Database.
5. **addGenre():** This method serves the addGenre.html page to add a new genre to the Database.
6. **editMovie(genre_id, movie_id):** This method serves the editMovie.html page for the creator of the movie to edit the movie.
7. **deleteMovie(genre_id, movie_id):** This method serves the deleteMovie.html page for the creator of the movie to delete the movie.
8. **login():** Serves the login page and creates the Anti-Forgery token.
9. **logout():** Removes the user from the session.
10. **fbconnect:** For Authenticating the user who used Facebook for accessing the application.
11. **fbdisconnect:** For revoking the user's Authentication token provided by FB.
10. **gconnect:** For Authenticating the user who used Google for accessing the application.
11. **gdisconnect:** For revoking the user's Authentication token provided by Google.

## Supporting Materials and Biblography:

The Project was developed as part of full-stack-nano-degree program provided by Udacity and the information for Virtual Machine setup using Virtual Box and Vagrant shared above([VM](https://github.com/udacity/fullstack-nanodegree-vm/blob/master/README.md)) is provided by Udacity.

For Styling Milligram Framework for CSS was used and the documentation for the same is available @([Milligram](https://milligram.io/))