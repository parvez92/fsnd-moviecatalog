from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dataBase_Setup import UserDetails, MovieCategory, MovieDetails, Base

engine = create_engine('sqlite:///catalogformovies.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
adduser1 = UserDetails(users_name="Parvez Hussain", users_email="parvez@udacity.com",
             users_image='https://commons.wikimedia.org/wiki/File:Udacity_logo.png')
session.add(adduser1)
session.commit()

# movies for Action
MovieCategory1 = MovieCategory(genre="Action", users_id=1)

session.add(MovieCategory1)
session.commit()

movie1 = MovieDetails(name="GoldenEye", users_id=1, description="James Bond teams up with the lone survivor of a destroyed Russian research center to stop the hijacking of a nuclear space weapon by a fellow Agent formerly believed to be dead.", moviecategory=MovieCategory1)

session.add(movie1)
session.commit()

movie2 = MovieDetails(name="Tomorrow Never Dies", users_id=1,  description="James Bond heads to stop a media mogul's plan to induce war between China and the UK in order to obtain exclusive global media coverage.", moviecategory=MovieCategory1)

session.add(movie2)
session.commit()

movie3 = MovieDetails(name="Casino Royale", users_id=1, description="Armed with a license to kill, Secret Agent James Bond sets out on his first mission as 007, and must defeat a private banker to terrorists in a high stakes game of poker at Casino Royale, Montenegro, but things are not what they seem.", moviecategory=MovieCategory1)

session.add(movie3)
session.commit()

# movies for Animation
MovieCategory2 = MovieCategory(genre="Animation", users_id=1)

session.add(MovieCategory2)
session.commit()

movie1 = MovieDetails(name="The Lion King", users_id=1, description="As a cub, Simba is forced to leave the Pride Lands after his father Mufasa is murdered by his wicked uncle, Scar. Years later, he returns as a young lion to reclaim his throne.", moviecategory=MovieCategory2)

session.add(movie1)
session.commit()

movie2 = MovieDetails(name="Beauty and the Beast", users_id=1,  description="Belle, a beautiful young woman, agrees to live with the Beast in exchange for the return of her abducted father. Soon, Belle discovers that her hideous captor is actually an enchanted prince.", moviecategory=MovieCategory2)

session.add(movie2)
session.commit()

movie3 = MovieDetails(name="Toy Story", users_id=1, description="Andy's favourite toy, Woody, is worried that after Andy receives his birthday gift, a new toy called Buzz Lightyear, his importance may get reduced. He thus hatches a plan to eliminate Buzz.", moviecategory=MovieCategory2)

session.add(movie3)
session.commit()

# movies for Adventure
MovieCategory3 = MovieCategory(genre="Adventure", users_id=1)

session.add(MovieCategory3)
session.commit()

movie1 = MovieDetails(name="Back to the Future", users_id=1, description="Marty McFly, a 17-year-old high school student, is accidentally sent thirty years into the past in a time-traveling DeLorean invented by his close friend, the maverick scientist Doc Brown.", moviecategory=MovieCategory3)

session.add(movie1)
session.commit()

movie2 = MovieDetails(name="Back to the Future Part II", users_id=1, description="After visiting 2015, Marty McFly must repeat his visit to 1955 to prevent disastrous changes to 1985...without interfering with his first trip.", moviecategory=MovieCategory3)

session.add(movie2)
session.commit()

movie3 = MovieDetails(name="Back to the Future Part III", users_id=1, description="Enjoying a peaceable existence in 1885, Doctor Emmet Brown is about to be killed by Buford Mad Dog Tannen. Marty McFly travels back in time to save his friend.", moviecategory=MovieCategory3)

session.add(movie3)
session.commit()

# movies for Crime
MovieCategory4 = MovieCategory(genre="Crime", users_id=1)

session.add(MovieCategory3)
session.commit()

movie1 = MovieDetails(name="The Godfather", users_id=1, description="The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.", moviecategory=MovieCategory4)

session.add(movie1)
session.commit()

movie2 = MovieDetails(name="Pulp Fiction", users_id=1, description="The lives of two mob hitmen, a boxer, a gangster's wife, and a pair of diner bandits intertwine in four tales of violence and redemption.", moviecategory=MovieCategory4)

session.add(movie2)
session.commit()

movie3 = MovieDetails(name="The Dark Knight", users_id=1, description="When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham. The Dark Knight must accept one of the greatest psychological and physical tests of his ability to fight injustice.", moviecategory=MovieCategory4)

session.add(movie3)
session.commit()