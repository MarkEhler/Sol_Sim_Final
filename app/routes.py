from flask import render_template, flash, redirect, url_for, send_file, request, Response
from app import app
from app.forms import SimForm
from app.api_calls import *
import time
from io import StringIO
import io, random
# draw figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

@app.route('/')
@app.route('/dashboard', methods=['GET', 'POST'])
def form():
	form = SimForm()
	if form.validate_on_submit():
		# date_ = form.date.data
		# location_ = form.location.data
		# time_span_ = form.time_span.data
		flash(f'Building graph for {form.time_span.data} days...') #success, add css
		return redirect(url_for('results'))
	return render_template('form.html', title='Check Yo Place!', form=form)

@app.route('/about', methods=['GET', 'POST'])
def about():
	return render_template('about.html', title='About')

@app.route('/results', methods=['GET', 'POST'])
def handle_data():
	output, sunrise, sunset = loop_data_collect(int(request.form['time_span']), request.form['location'], request.form['date'])
	day_dict = process(output, int(request.form['time_span']), sunrise, sunset)
	return render_template('results.html', title=' sunny day(s)')











@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure(final_data, days):
	    '''
    takes a feature array and plots it against the time index and 
    time_span = days.unique
    converts minutes in integer form into into a clock reading for ease of translation
    '''
    plt.style.use('seaborn')
    fig = Figure(figsize=(30,15*days))
    # canvas = FigureCanvas(fig)
    x = [convert_minutes(time, forward=False, seconds=False) for time in final_data[1].index]
    for day in range(days):
        axis = fig.add_subplot(len(range(days)), 1, day+1) # mirror subplots in plot fx
        axis.plot(x, final_data[day+1].Output, label='Photovoltaic Energy Produced',
                    color='orange', fillstyle='bottom')
        axis.set_xlabel('Time', fontdict = {'fontsize' : 20})
        axis.set_ylabel('W/m^2', fontdict = {'fontsize' : 20})
        axis.legend(loc='upper left')
        axis.set_title(f'Day {day+1}', fontdict = {'fontsize' : 24}, loc= 'left')
        for tick in axis.xaxis.get_major_ticks():
            tick.label.set_fontsize(14) 
            tick.label.set_rotation('vertical')
        for tick in axis.yaxis.get_major_ticks():
            tick.label.set_fontsize(22) 

    return fig
















# @app.route('/return-file/')
# def get_images():
#     return send_file('C://Users//Mark//Documents//DataSci//Module 5//FLASK//flask_dashboard//solar_dashboard//app//static//sun_plot2.png', attachment_filename = 'test')

# @app.route('/file-download/')
# def images():
# 	return render_template("images.html")






































































# @app.route('/plot')
# def plot(chartID = 'chart_ID', chart_type = 'bar', chart_height = 350):
# 	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
# 	series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
# 	title = {"text": 'My Title'}
# 	xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
# 	yAxis = {"title": {"text": 'yAxis Label'}}
# 	return render_template('plt.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)




