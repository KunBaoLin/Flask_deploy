from flask import render_template, session,flash,redirect, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.band import Band


@app.route('/new/band') # route to create band
def new_band():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_band.html',user=User.get_by_id(data))


@app.route('/create/band',methods=['POST'])  #create new band
def create_band():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Band.validate_band(request.form):
        return redirect('/new/band')
    data = {
        "name": request.form["name"],
        "genre": request.form["genre"],
        "city": request.form["city"],
        "user_id": session["user_id"]
    }
    Band.save(data)
    return redirect('/dashboard')

@app.route('/edit/band/<int:id>') # route to edit band
def edit_band(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_band.html",edit=Band.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/band/<int:id>',methods=['POST']) #update band
def update_band(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Band.validate_band(request.form):
        return redirect(f'/edit/band/{id}')
    data = {
        "id": request.form['id'],
        "name": request.form["name"],
        "genre": request.form["genre"],
        "city": request.form["city"],
    }
    Band.update(data)
    return redirect('/dashboard')


@app.route('/destroy/band/<int:id>', methods = ['post']) #destroy band
def destroy_band(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Band.destroy(data)
    return redirect('/dashboard')
