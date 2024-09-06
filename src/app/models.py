from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    preference = db.Column(db.String)
    value = db.Column(db.String)


class Paper(db.Model):
    __tablename__ = 'papers'
    id = db.Column(db.Integer, primary_key=True)
    arxiv_id = db.Column(db.String, unique=True, nullable=False)  # Unique identifier on arXiv
    title = db.Column(db.String, nullable=False)  # Title of the paper
    authors = db.Column(db.Text, nullable=False)  # List of authors, stored as a comma-separated string
    abstract = db.Column(db.Text, nullable=False)  # Abstract of the paper
    categories = db.Column(db.String, nullable=False)  # Categories the paper belongs to
    comments = db.Column(db.String)  # Additional comments (e.g., "10 pages, 5 figures")
    doi = db.Column(db.String)  # DOI of the paper, if available
    journal_ref = db.Column(db.String)  # Journal reference, if the paper is published
    report_no = db.Column(db.String)  # Report numbers associated with the paper
    submission_history = db.Column(db.Text)  # Submission history (versions and dates)
    created = db.Column(db.String, nullable=False)  # Original submission date
    updated = db.Column(db.String)  # Last updated date for the submission
    license = db.Column(db.String)  # License under which the paper is published
    link = db.Column(db.String, nullable=False)  # Link to the paper on arXiv

    def to_dict(self):
        return {
            'id': self.id,
            'arxiv_id': self.arxiv_id,
            'title': self.title,
            'authors': self.authors,
            'abstract': self.abstract,
            'categories': self.categories,
            'comments': self.comments,
            'doi': self.doi,
            'journal_ref': self.journal_ref,
            'report_no': self.report_no,
            'submission_history': self.submission_history,
            'created': self.created,
            'updated': self.updated,
            'license': self.license,
            'link': self.link
        }



class UserEvent(db.Model):
    __tablename__ = 'user_events'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # ID of the user
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.id'), nullable=False)  # ID of the paper
    event_type = db.Column(db.String, nullable=False)  # Type of interaction (e.g., 'viewed', 'liked', 'shared')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # When the event occurred

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'paper_id': self.paper_id,
            'event_type': self.event_type,
            'timestamp': self.timestamp.isoformat()
        }