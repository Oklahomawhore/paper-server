from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        # Import and register routes
        from .routes import user_routes, paper_routes, user_event_routes
        app.register_blueprint(user_routes.bp)
        app.register_blueprint(paper_routes.bp)
        app.register_blueprint(user_event_routes.bp)

        # Create tables
        db.create_all()

        # Initialize the scheduler
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=schedule_arxiv_scraping, trigger="interval", hours=24)
        scheduler.start()

        # Shut down the scheduler when exiting the app
        import atexit
        atexit.register(lambda: scheduler.shutdown())

        
    with app.test_request_context():
        print(url_for('user.register'))
    

    return app

def schedule_arxiv_scraping():
    """
    Function to scrape papers from ArXiv and save to the database.
    Adjust the query and max_results as per your needs.
    """

    from app.services.paper_service import fetch_and_store_papers_from_oai
    fetch_and_store_papers_from_oai()