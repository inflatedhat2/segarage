from flask import render_template, flash, redirect, url_for, send_from_directory, request
from flask_paginate import Pagination, get_page_parameter

from app import app
from app import db
from app.forms import requestToolUpload, toolUpload
from app.models import Paper, Tag, File
from app.utils import *

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html', greeting="You can upload your tool by clicking the above 'Request Upload' button")

@app.route('/request_upload', methods=['GET', 'POST'])
def request_upload():
  form = requestToolUpload()
  if form.validate_on_submit():
    token = get_email_token(form.authoremail.data, form.papername.data)

    text_body=render_template('email/link_to_upload.txt', token=token)
    html_body=render_template('email/link_to_upload.html', token=token)

    send_email('Link to upload tool', app.config['ADMIN'], ['scrawler16.1@gmail.com'], text_body, html_body)

    flash('Link to upload the tool has been sent to {} for the paper {}'.format(form.authoremail.data, form.papername.data))
    return redirect(url_for('index'))
  return render_template('request_upload.html', title='Request to upload Tool', form=form)

@app.route('/tool_upload/<token>', methods=['GET', 'POST'])
def tool_upload(token):

  payload = verify_email_token(token)
  if not payload:
    return redirect(url_for('index'))

  form = toolUpload()
  form.authoremail.data = payload['authoremail']

  if form.validate_on_submit():
    paper = Paper(paper_name=form.papername.data, author_name=form.authorname.data, author_email=form.authoremail.data, tool_name=form.toolname.data, link_to_pdf=form.linktopdf.data, link_to_archive=form.linktoarchive.data, link_to_tool_webpage=form.linktotoolwebpage.data, link_to_demo=form.linktodemo.data, bibtex=form.bibtex.data)

    print(form.tags.data)

    for tag in form.tags.data.split(","):
      tag_obj = db.session.query(Tag).filter(Tag.tagname==tag.strip()).first()
      if tag_obj is None:
        tag_obj = Tag(tagname=tag.strip())
      paper.tags.append(tag_obj)

    db.session.add(paper)
    db.session.flush()

    filenames = []

    ## Readme file upload
    if form.readme_file.data:
      save_file(form.readme_file, paper.id)
      filenames.append(secure_filename(form.readme_file.data.filename))
    # else:
    #   filenames = "None;"
    #   print("None shouldn't get stored ideally (readme)")


    ## Binary zip upload
    if form.binary_file.data:
      save_file(form.binary_file, paper.id)
      filenames.append(secure_filename(form.binary_file.data.filename))
    # else:
    #   filenames = filenames + "None;"
    #   print("None shouldn't get stored ideally (tool)")


    ## source upload
    if form.scripts_file.data:
      save_file(form.scripts_file, paper.id)
      filenames.append(secure_filename(form.scripts_file.data.filename))
    # else:
    #   filenames = filenames + "None"

    print("Uploaded files below for paper: {}".format(paper.id))
    print(filenames)

    for filename in filenames:
      paper.files.append(File(filename=filename))

    db.session.flush()
    db.session.commit()
    flash('Tool submission success {}'.format(paper.id))

    return redirect(url_for('index'))
    
  return render_template('tool_upload.html', title="Upload your tool here", form=form)


@app.route('/downloads/<id>/<filename>', methods=['GET', 'POST'])
def downloads(id, filename):
  print("Resource id: {}".format(id))
  print("Filename: {}".format(filename))
  print("Dir: {}".format(app.config['UPLOAD_FOLDER'] + "/{}".format(id)))
  return send_from_directory(app.config['UPLOAD_FOLDER'] + "/{}".format(id), filename, as_attachment=True)

@app.route('/papers')
def papers():
  search = False
  q = request.args.get('q')
  if q:
    search = True
  page = request.args.get(get_page_parameter(), type=int, default=1)

  papers = Paper.query.all()
  print('Total number of papers: {}'.format(len(papers)))
  pagination = Pagination(page=page, total=len(papers), search=search, record_name='papers')

  return render_template('papers.html', papers=papers, pagination=pagination)
