from flask import render_template, flash, redirect, url_for, request, Response, session
from app import app
from app.forms import SimForm
from app.api_calls import *
import os, io, json
# draw figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


# session = ('listed': None)

@app.route('/')
@app.route('/dashboard', methods=['GET', 'POST'])
def form():
	form = SimForm()
	if form.validate_on_submit():
		flash(f'Building graph for {form.time_span.data} days...')
		return redirect(url_for('results'))
	return render_template('form.html', title='Check Yo Place!', form=form)

@app.route('/about')
def about():
	return render_template('about.html', title='About')

@app.route('/results', methods=['GET', 'POST'])
def handle_data():
    output, sunrise, sunset = loop_data_collect(int(request.form['time_span']), request.form['location'], request.form['date'])
    avg, daily_mean, hours_daylight = daily_mean(output)
    for i in range(7):
        session.pop(str(i), None)
    listed, session['time'] = process(output, int(request.form['time_span']), sunrise, sunset)
    for i in enumerate(listed):
        session[str(idx)] = i
    return render_template('results.html', title='Sunny Day(s)')


@app.route('/plot.png')
def plot_png():
    fig = create_figure(session)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

# option to hard code time index for plot
# remeber to subtract one from len of session object for the time
def create_figure(session_obj):
    fig = Figure(figsize=(10,3*len(session_obj)))
    times = json.loads(session_obj['time']) # should be in json format and needs to be changed
    x = [convert_minutes(session_obj['time'], forward=False, seconds=False) for time in times]
    for i in range(len(session_obj)):
        day = pd.read_json(session_obj[str(i)], typ='series')
        day = day.sort_index()
        axis = fig.add_subplot(1, 1, 1)
        axis.plot(x, day, label='Photovoltaic Energy Produced',
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


def process(final_data, days, sunrise, sunset):
    '''
    runs the returned data on the trained model.
    each day returns a list of W/m^2 outputs which are then used to get some relavent information for the user:
    daily totals.
    '''
    days = int(days)
    cols = final_data.columns.to_list()
    feature_cols = cols[:5] + cols[-1:]
    model = os.path.join(os.getcwd(), 'app//static', 'final_model.pkl')
    scaler = os.path.join(os.getcwd(), 'app//static', 'final_scaler.pkl')
    loaded_day_model = pickle.load(open(model, 'rb'))
    loaded_day_scaler = pickle.load(open(scaler, 'rb'))

    sunrise_minutes = (convert_minutes(sunrise, forward=True, seconds=True) // 15)
    sunset_minutes = (convert_minutes(sunset, forward=True, seconds=True) // 15)
       
    feats = final_data.loc[:,feature_cols]
    features = loaded_day_scaler.transform(feats)
    output = loaded_day_model.predict(features)
#     because the government site the zenith angle was scraped from does not distingush between degrees above the horizon (+)
#     and degrees below the horizon (-) there is a chance that some night time data will return a small positive number
#     in the most up-to-date itteration there doesn't seem to be much of a need for this but still, for safety
    output = output.clip(min=0)
    final_data['Output'] = output
    dayz = final_data.Day.unique()
    listed = []
    times = list(output_copy.index)
    times = json.dumps([convert_minutes(time, seconds=False) for time in times])
    for day in dayz:
        day = final_data[final_data.Day == day]
#         day[:sunrise_minutes] = 0
#         day[sunset_minutes:] = 0
        day = day['Output'].to_json()
        listed.append(day)
 
    return listed, times





# @app.route('/return-file/')
# def get_images():
#     return send_file('C://Users//Mark//Documents//DataSci//Module 5//FLASK//flask_dashboard//solar_dashboard//app//static//sun_plot2.png', attachment_filename = 'test')

# @app.route('/file-download/')
# def images():
# 	return render_template("images.html")





# def create_figure():
#     fig = Figure()
#     axis = fig.add_subplot(1, 1, 1) # mirror subplots in plot fx
#     xs = [1,2,3,4]
#     ys = [1,2,3,4]
#     axis.scatter(xs, ys)
#     return fig






# @app.route('/plot')
# def plot(chartID = 'chart_ID', chart_type = 'bar', chart_height = 350):
# 	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
# 	series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
# 	title = {"text": 'My Title'}
# 	xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
# 	yAxis = {"title": {"text": 'yAxis Label'}}
# 	return render_template('plt.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)