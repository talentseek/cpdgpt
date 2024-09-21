import os

class Config:
    SMARTLEAD_API_KEY = "84317e41-800f-43e4-9bed-d00961eae992_yb1fzb8"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.getcwd()), 'cpdadmin.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False  # Disable CSRF protection
    # Add Secret Key for CSRF Protection
    SECRET_KEY = 'ht%/XUa|A4])Fi)6j;W2'  # Replace with your actual secret key
    WTF_CSRF_SECRET_KEY = SECRET_KEY  # CSRF protection uses the same secret key