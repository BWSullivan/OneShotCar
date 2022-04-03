from flask import render_template
#from datetime import datetime*

@app.route('/')
def test():
    #current_time = datetime.now().strftime('%H:%M:%S')
    return render_template('base.html',name='nnnnnn', time=1)