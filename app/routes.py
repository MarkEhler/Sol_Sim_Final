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
    for i in range(7):
        session.pop(str(i), None)
    session.pop('time', None)
    listed, session['time'], avgs = process(output, int(request.form['time_span']), sunrise, sunset)
    for idx, i in enumerate(listed):
        session[str(idx)] = i
        print(idx)
            # avg, daily_mean, hours_daylight = daily_avg(output)
    return render_template('results.html', title='Sunny Day(s)', avgs=avgs)


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
    times = json.loads(session_obj['time'])
    counter = 1
    while counter < (len(session_obj) - 1):
        for idx, i in enumerate(session_obj):
            print(idx)
            day = pd.read_json(session_obj[str(idx)], typ='series')
            day = day.sort_index()
            axis = fig.add_subplot(1, 1, 1)
            axis.plot(times, day, label='Photovoltaic Energy Produced',
                    color='orange', fillstyle='bottom')
            axis.set_xlabel('Time', fontdict = {'fontsize' : 20})
            axis.set_ylabel('Watt per Square Meter of Panels', fontdict = {'fontsize' : 20})
            axis.legend(loc='upper left')
            axis.set_title(f'Day {idx+1}', fontdict = {'fontsize' : 24}, loc= 'left')
            for tick in axis.xaxis.get_major_ticks():
                tick.label.set_fontsize(8) 
                tick.label.set_rotation(65)
            for tick in axis.yaxis.get_major_ticks():
                tick.label.set_fontsize(22)
            counter += 1
    return fig


def process(final_data, days, sunrise, sunset):
    '''
    runs the returned data on the trained model.
    each day returns a list of W/m^2 outputs which are then used to get some relavent information for the user:
    daily totals.
    returns a list of output values, a time_index session object, and a list of averages tuples
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
    averages = []
    times = list(final_data.index)
    times = json.dumps([convert_minutes(time, seconds=False) for time in times[:96]])
    for day in dayz:
        day = final_data[final_data.Day == day]
        #         day[:sunrise_minutes] = 0
        #         day[sunset_minutes:] = 0
        averages.append((daily_avg(day)))
        day = day['Output'].to_json()
        listed.append(day)

    return listed, times, averages
