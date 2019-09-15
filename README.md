<h1> Sol-Sim Solar Energy Tool </h1>
<h2> TOC </h2>
<ul>
    <li> app/ -- flask package files</li>
    <li> run.py -- init file for flask package </li>
    <li> demo video place holder </li>
    <li> </li>
    <li> </li>
    <li> </li>
    <li> </li>
</ul>
<h2> Clearing the Skies of Solar Energy </h2>
    It was while thinking about human rights that I got the idea for this project.  Power is something we, as Americans take for granted.  "Where does it come from when I flip on the switch?" Isn't a question most of us think about, nor should we.  Our children don't have to think about the billion dollar industry that supplies them with air conditioned schools.  We ourselves have become addicted, not so much to screens, as the passage of electrons through our devices that lights them up.  After all, our social media accounts will survive without our need to check on them.   <br><br>
    It's no wonder that the energy debate is a polarizing one. At the time of writing this gas and oil companies are advertising that renewable energy's main detraction is it's unreliability.  I think this is a false perception.  If there is one thing I've learned from working with weather data, it's that people will never beat the machine in recalling historical weather data. It's fortunate that we have decades of weather data recorded; and even, solar energy data.  Energy could be said to be surpassing other basic human rights in terms of profitability, and ethics of distribution becomes more and more center stage.<br><br>
    My goal with this project was to create a tool that could be used to give a machine informed plot of data for a specific location using solar and weather data to inform it's estimation. More insight into the ethos of this project can be found on my <a href="https://markehler.github.io/sol-sim_-_solar_energy_ethos"> blog </a> but the goal of this abtract is to familiarize you with the technical details of this app.
    My goal was to develop a prototype that could be further developed by a solar installation company or a tech service company providing renewable energy installers with tools to grow their business.  Similar products as this one do exist.  <a href="https://www.google.com/get/sunroof"> Project Sunroof </a> by Google and <a href="https://www.helioscope.com/"> Helioscope </a> a paid for software solution by Folsom Labs.  While Project Sunroof has taken account for what the industry calls a "shade analysis", it does not seem to adjust for Latitude and weather factors.  It's my belief that the two apps could be used in tandem by solar hopefuls to inform their renewable decision.
<br>
<br>
<h2> It's Simple Astronomy </h2>
<h3> Data Harvested Piecemeal </h3>
    All data was collected individually from <a href="https://midcdmz.nrel.gov/">NREL</a> test sites across the United States. This took a fair amount of cajoling because each site uniquely labeled their data, most of them sensing unique values from one another that had to be converted or ignored.
    <a href="https://imgur.com/cM4lShX"><img src="https://i.imgur.com/cM4lShX.jpg" title="NREL" width="250" height="100", STYLE = "float: right;"> </a>
<br>
      Ultimately, it was important and reliable to collect the solar angles the sun traces across the sky and the temp.  Later, known latitude and longitude of each site was added in.  It would be possible, with more time and effort, to collect more weather data keyed off of a datetime index using nearby weather stations.  
<h3> Icarus Was Right</h3>
    Very quickly when looking at the sun we find that at the center of our solar system lies a very large nuclear clock.  The graphs of geometric values returned from the test sites having watched the sun were so beautiful to a statistician, almost too beautiful.  It turns out that renewable energy is indeed reliable and hard to argue against.    <br><a href="https://imgur.com/YKPgEq5"><img src="https://i.imgur.com/YKPgEq5.png" title="user input features" width="250" height="500", STYLE = "float: right;"></a><br>
    The Sun, undeniably the most important factor in generating solar energy, is
so reliable that astronomers can calculate where the great ball of fire will be in the sky at any time for any place.  This produces wonderfully normal distributions of the sun's location in the sky.  After doing feature analysis on some decision tree models, it is clear that the most important thing in solar production is where the sun is located.  The industry knows this, so when installing new solar panels we look for what is called a 'solar window', a box in the sky that the sun travels through most of the days throughout most of the year. <br>  
<a href="https://imgur.com/GkfSb4l"><img src="https://i.imgur.com/GkfSb4l.png" title="feature heatmap" width="450" height="300", STYLE = "float: center;" /></a>
<h3> Unexpected Scattered Showers </h3>
    While working on this project there were a few sticking points.  As it turns out, there are two ways of calculating Zenith angle.  This project uses topocentric, meaning that there is no account for the sun's angle above or below the horizon, it will look the same either way.  The model does an okay job accounting for this but nonetheless night time values were silenced on the final graph.  Certain categorical features could be expressed with their own columns for getter accuracy but since I want to app to predict on locations that aren't present in the dataset, they have been left as float variables rather than one hot encoded as i would like to do.  <br><br>    
       I learned on this project that my most accurate model upon initial training, which was accurate to 80 Watts per meter squared, produced downright wacky plots when tested against newly gathered data user input.<a href="https://imgur.com/wQ8AgxS"><img src="https://i.imgur.com/wQ8AgxS.png" title="wonky data" width="375" height="200", STYLE = "float: left;" /></a> <br>**Why was that?**<br>  Accuracy, as it turns out, isn't everything.  I found that my dataset could not possibly account for all the factors accounting for solar energy from entirely new locations.  In other words, my model had overfit.  As I slackened the accuracy by 15 - 20 Watts per meter squared I found that my plots looked a lot more reasonable.  What's more important, they still seemed responsive to the weather.  In the end I was able to reclaim this accuracy by fine tuning my data, not my parameters, a key lesson in garbage in garbage out.  Error is resting at 77W/m^2 after 3 cross validations at the time of publishing. <br>
<h3> The Sun Never Sleeps When it's Light Out </h3>
    I'm still suspicious of my final model and would like to revise it before shipping as a for-profit tool.  What I would expect would be a normal distribution of energy production.  The hours from 9am to 3pm are known to produce peak power for energy that tapers while the sun is rising and setting.  I had the solar equivalent of unhealthy self-body-image upon launching my tool below.<br>
    <a href="https://imgur.com/QLlD4tR"><img src="https://i.imgur.com/GZuaz1N.png" title="first working plot" width="500" height="500", location = "right" /></a>
    <a href="https://imgur.com/wF2MhIn"><img src="https://i.imgur.com/wF2MhIn.png" title="test site calendar" width="400" height="400", location = "left" /></a>
    Above is a calendar from one of the test sites I used for sourcing my data.  The three lines represent different types of received solar radiation.  The one we are most concerned with is the red line. Knowing that I'm under reporting on weather data,  I'm left with the astronomy of the sun as my most important features.  I'm hard on myself but happy with this as a live app prototype.  My main goal with this project was to educate, so if the sim needs a little refinement I can easily work on it.  Rather, the focus should be on this apps ability to take complex astronomy and apply for practical use.  I should hope that the app will speak for itself in that regard.<br><br>
    The natural gas industry will boast that their fuel burning plants are reliable.  I would argue that the sun that has reliably powered life on this planet for eons will still be reliable even when the coal plants come tumbling down at the end of their shelf life. 
