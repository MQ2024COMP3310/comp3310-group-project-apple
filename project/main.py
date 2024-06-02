from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory, current_app
from flask_login import login_required, current_user
from .models import Photo
from sqlalchemy import asc, or_
from . import db
import os

main = Blueprint('main', __name__)

@main.route('/')
def homepage():
    if current_user.is_authenticated:
        # Show public photos and private photos owned by the current user
        photos = db.session.query(Photo).filter(
            or_(Photo.private == False, Photo.user_id == current_user.id)
        ).order_by(asc(Photo.file)).all()
    else:
        # Only show public photos
        photos = db.session.query(Photo).filter_by(private=False).order_by(asc(Photo.file)).all()
    return render_template('index.html', photos=photos)

@main.route('/uploads/<name>')
def display_file(name):
    return send_from_directory(current_app.config["UPLOAD_DIR"], name)

@login_required  # (secure coding principles) authenticated user only can upload a photo
@main.route('/upload/', methods=['GET', 'POST'])
def newPhoto():
    if not current_user.is_authenticated:  # (secure coding principles) only authenticated user can upload a photo
        flash("You must be logged in to upload photos.", "error")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        file = request.files.get("fileToUpload")
        if not file or not file.filename:
            flash("No file selected!", "error")
            return redirect(request.url)

        filepath = os.path.join(current_app.config["UPLOAD_DIR"], file.filename)
        file.save(filepath)
       
        # (secure coding principles) Save user_id of the uploader
        newPhoto = Photo(name=current_user.email, 
                         caption=request.form['caption'],
                         description=request.form['description'],
                         file=file.filename,
                         user_id=current_user.id,
                         private='private' in request.form)
        db.session.add(newPhoto)
        db.session.commit()
        flash('New Photo %s Successfully Created' % newPhoto.name)
        return redirect(url_for('main.homepage'))
    else:
        return render_template('upload.html')

@login_required # (secure coding principles) user can edit a photo that user own
@main.route('/photo/<int:photo_id>/edit/', methods=['GET', 'POST'])
def editPhoto(photo_id):
    editedPhoto = db.session.query(Photo).filter_by(id=photo_id).one()
    if current_user.is_anonymous or (current_user.id != editedPhoto.user_id and not current_user.is_admin):
        flash('You do not have permission to edit this photo.', 'error')
        return redirect(url_for('main.homepage'))

    if request.method == 'POST':
        editedPhoto.name = request.form['user']
        editedPhoto.caption = request.form['caption']
        editedPhoto.description = request.form['description']
        db.session.add(editedPhoto)
        db.session.commit()
        flash('Photo Successfully Edited %s' % editedPhoto.name)
        return redirect(url_for('main.homepage'))
    else:
        return render_template('edit.html', photo=editedPhoto)

@login_required # user can delete a photo that user own
@main.route('/photo/<int:photo_id>/delete/', methods=['GET', 'POST'])
def deletePhoto(photo_id):
    deletedPhoto = db.session.query(Photo).filter_by(id=photo_id).one()
    if current_user.is_anonymous or (current_user.id != deletedPhoto.user_id and not current_user.is_admin): 
        flash('You do not have permission to delete this photo.', 'error')
        return redirect(url_for('main.homepage'))

    filename = deletedPhoto.file
    filepath = os.path.join(current_app.config["UPLOAD_DIR"], filename)
    os.unlink(filepath)
    db.session.delete(deletedPhoto)
    db.session.commit()

    flash('Photo id %s Successfully Deleted' % photo_id)
    return redirect(url_for('main.homepage'))

# Task 9 implementation for Photos are searchable using keywords from the metadata
# Add a new route for searching photos
@main.route('/search', methods=['GET'])
def search_photos():
    query = request.args.get('query')
    if not query:
        flash("Please enter a search term.", "error")
        return redirect(url_for('main.homepage'))

    # photo can be searched with the name, caption, and description in seaching bar 
    # (secure coding principles) using parameterized queries to prevent SQL injection
    search = "%{}%".format(query)
    if current_user.is_authenticated:
        # Show public photos and private photos owned by the current user
        photos = db.session.query(Photo).filter(
            or_(
                Photo.name.ilike(search),
                Photo.caption.ilike(search),
                Photo.description.ilike(search)
            ),
            or_(
                Photo.private == False,
                Photo.user_id == current_user.id
            )
        ).order_by(asc(Photo.file)).all()
    else:
        # Only show public photos
        photos = db.session.query(Photo).filter(
            or_(
                Photo.name.ilike(search),
                Photo.caption.ilike(search),
                Photo.description.ilike(search)
            ),
            Photo.private == False  # Exclude private photos
        ).order_by(asc(Photo.file)).all()

    return render_template('index.html', photos=photos)