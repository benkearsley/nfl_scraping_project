# nfl_scraping_project

11/21/23.  

At this point in our project, we have successfully scraped and transformed play by play data from each game during week 10 of the 2023 NFL season.  We scraped it from www.pro-football-reference.com, and are building a couple different files that can be joined together to create the data we are using for the project.  Currently, this includes a games table and a plays table.  We have also added columns to make it easier to analyze the data and move our project forward.  For example, we added columns to represent the size of the field, the yardage from the play, and who posesses the ball.  We are also working on adding columns to represent the one or two primary players involved in the offense on each play, and to classify plays as pass or run or special teams.

Once the dataset is completely clean, we will be working on the analysis portion of our project.  We are still considering a couple different options for our analysis:

# 1 Visualization Focus

This would mean focusing on visualizing the play by play data in a novel way.  We could visualize things like player involvement and even expected points per play.  This would involve building an interface with Plotly Dash, and then building filtering mechanisms and different ways to bring in specific data from games so that users can view the data that they want and not just what we have scraped.

# 2 Modeling Focus

This focus would look more at trying to predict different outcomes from the play by play data.  One idea might be trying to develop our own prediction of who will win or lose (almost like what ESPN does, but probably a little different; we could even compare it to their metric throughout the game and see how good we do).  There are other things we could try to predict or classify as well, but I think this might be one challenge that we face.  

As the semester starts wrapping up, we are excited to wrap up this package and turn it into something that sports fans can use to understand and study their favorite teams in more detail than ever.  Now that the data is clean and ready, the real fun stuff can start!
