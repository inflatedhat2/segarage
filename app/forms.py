from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, MultipleFileField, SelectField
from wtforms.validators import InputRequired, DataRequired, Email, ValidationError

from app.utils import allowed_files, FILETYPE_CHOICES

def file_validation(form, field):
  if field.data:
    for file in field.data:
      if isinstance(file, str):
        continue
      if not allowed_files(file.filename):
        raise ValidationError('File format not supported (supported: md, txt, pdf, docx, zip, gz, rar)')

class requestToolUpload(FlaskForm):
  authoremail = StringField('Contact author Email', validators=[DataRequired(), Email('Please enter valid email address')])
  papername = StringField('Paper Name', validators=[DataRequired()])

  recaptcha = RecaptchaField()
  request_upload = SubmitField('Need to upload tool for the paper')

class toolUpload(FlaskForm):
  toolname = StringField('Tool name')

  papername = StringField('Paper Title', validators=[DataRequired()])
  authorname = StringField('Contact author Name')
  authoremail = StringField('Contact author Email', validators=[DataRequired(), Email('Please enter valid email address')])

  linktopdf = StringField('Link to publicly available version of the paper')
  linktoarchive = StringField('Link to published version (ACM/IEEE/peerJ etc.,)', validators=[DataRequired()])
  linktotoolwebpage = StringField('Link to tool webpage')
  linktodemo = StringField('Link to demo (youtube)')

  bibtex = TextAreaField('BibTex entry', validators=[DataRequired()])

  # readme_file = FileField('Upload Readme or instructions file', validators=[DataRequired(), txt_file_check])
  # scripts_file = FileField('Upload source code (optional)', validators=[zip_file_check])
  # binary_file = FileField('Upload final version of the tool (binary)', validators=[DataRequired(), zip_file_check])

  choices = [(item, item) for item in FILETYPE_CHOICES]
  dropdown_choices = SelectField(choices=choices)
  file_types = StringField()

  all_files = MultipleFileField('Upload your files (readme, binary, script etc.,)', validators=[DataRequired(), InputRequired(), file_validation])

  tags = StringField('Tags', validators=[DataRequired()])

  upload = SubmitField('Upload')