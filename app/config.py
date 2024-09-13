import os

class Config:
    SMARTLEAD_API_KEY = "84317e41-800f-43e4-9bed-d00961eae992_yb1fzb8"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.getcwd()), 'cpdadmin.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
