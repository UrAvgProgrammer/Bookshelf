from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators



class Forms(Form):
    titleNew = StringField('Title', [validators.Length(min=1,max=60)])
    yearNew = StringField('Year Published', [validators.Length(min=1,max=60)])
    typeNew = StringField('Book Type', [validators.Length(min=1,max=60)])
    authorNew = StringField('Author', [validators.Length(min=1,max=60)])
    editionNew = StringField('Edition', [validators.Length(min=1,max=60)])
    isbnNew = StringField('ISBN', [validators.Length(min=1,max=60)])
    submit = SubmitField("Submit")

class BookForms(Form):
    bookidNew = StringField('Book ID', [validators.Length(min=1,max=60)])
    submit = SubmitField("Submit")

