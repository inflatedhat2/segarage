from flask import render_template, flash, redirect, url_for
from app import app
from app import db
from app.forms import requestToolUpload, toolUpload
from app.models import Paper
from app.utils import *

@app.route('/')
@app.route('/index')

def index():
  return render_template('index.html', greeting="What part of your research you want to offer the SE community, Tool/Scripts/Framework/Others?")

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
    paper = Paper(paper_name=form.papername.data, author_name=form.authorname.data, author_email=form.authoremail.data, tool_name=form.toolname.data, tool_format=form.toolformat.data, link_to_pdf=form.linktopdf.data, link_to_archive=form.linktoarchive.data, link_to_readme=form.linktoreadme.data, link_to_demo=form.linktodemo.data, bibtex=form.bibtex.data)

    db.session.add(paper)
    db.session.commit()
    flash('Tool submission success')
    return redirect(url_for('index'))
    
  return render_template('tool_upload.html', title="Upload your tool here", form=form)