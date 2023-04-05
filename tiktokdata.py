import os
import json
import argparse
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.movie import Movie
from models.user import User
from models.view import View
from models.share import Share
from models.like import Like
from tiktoktools import get_final_url, get_and_save_page
from trollrensicsapiclient import retrieve_tiktok_video_data

user = os.environ['MYSQL_USER']
password = os.environ['MYSQL_PASSWORD']
host = os.environ['MYSQL_HOST']
port = os.environ['MYSQL_PORT']
database = os.environ['MYSQL_DATABASE']

engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}', echo=False)

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    print("Creating database structure")
    inspector = inspect(engine)
    Movie.metadata.create_all(engine)
    User.metadata.create_all(engine)
    View.metadata.create_all(engine)
    Share.metadata.create_all(engine)
    Like.metadata.create_all(engine)
    print("Finished creating database structure")

def create_records():
    print("Reading data files")
    for filename in os.listdir('data'):
        if filename.endswith('.json'):
            print(f"- processing {filename}")
            with open(os.path.join('data', filename)) as f:
                data = json.load(f)

            user_id = filename.split('.')[0].split('_')[-1]

            user, created = User.get_or_create(session=session, id=user_id, username=user_id)
            if created:
                session.add(user)
                session.flush()

            for video in data['Activity']['Video Browsing History']['VideoList']:
                movie, created = Movie.get_or_create(session=session, sharelink=video['Link'])
                if created:
                    session.add(movie)
                    session.flush()

                view, created = View.get_or_create(session=session,
                    datetime=datetime.strptime(video['Date'], '%Y-%m-%d %H:%M:%S'),
                    user_id=user_id,
                    movie_id=movie.id
                )
                if created:
                    session.add(view)
            
            for video in data['Activity']['Like List']['ItemFavoriteList'] or []:
                movie, created = Movie.get_or_create(session=session, sharelink=video['Link'])
                if created:
                    session.add(movie)
                    session.flush()

                like, created = Like.get_or_create(session=session,
                    datetime=datetime.strptime(video['Date'], '%Y-%m-%d %H:%M:%S'),
                    user_id=user_id,
                    movie_id=movie.id
                )
                if created:
                    session.add(like)                    

            shares = data.get('Activity', {}).get('Share History', {}).get('ShareHistoryList', [])
            for video in shares:
                movie, created = Movie.get_or_create(session=session, sharelink=video['Link'])
                if created:
                    session.add(movie)
                    session.flush()

                share, created = Share.get_or_create(session=session,
                    datetime=datetime.strptime(video['Date'], '%Y-%m-%d %H:%M:%S'),
                    user_id=user_id,
                    movie_id=movie.id
                )
                if created:
                    session.add(share)  

    session.commit()
    session.close()
    print("Finished reading data files")


def retrieve_links():
    print("Resolving share links")
    movies = session.query(Movie).filter(Movie.tiktoklink.is_(None)).all()

    counter = 0
    for movie in movies:
        final_url = get_final_url(movie.sharelink)
        print(f"- resolved {movie.sharelink} to {final_url}")
        movie.tiktoklink = final_url
        
        counter += 1
        if counter % 10 == 0:
            session.commit()

    session.commit()
    session.close()
    print("Finished resolving share links")

def retrieve_videos():
    print("Retrieving TikTok videos")
    movies = session.query(Movie).filter(Movie.videolink.is_(None)).all()

    counter = 0
    for movie in movies:
        fi = retrieve_tiktok_video_data(movie.tiktoklink)
        movie.videolink = fi['filename']
        movie.description = fi['description'][:511]
        print(f"- retrieved {movie.tiktoklink} to {movie.videolink}")
        session.commit()
        counter += 1
        if counter % 10 == 0:
            session.commit()

    session.commit()
    session.close()
    print("Finished retrieviing TikTok videos")

def export_xlsx():
    print("Exporting to XLSX")
    query = "SELECT * FROM movies"
    movies_df = pd.read_sql_query(query, engine)
    output_file = "movies_table.xlsx"
    movies_df.to_excel(output_file, index=False, engine='openpyxl')
    print("Finished exporting to XLSX")

def main():
    parser = argparse.ArgumentParser(description="Parse and store TikTok data files")
    parser.add_argument("--create-db", action="store_true", help="Create database")
    parser.add_argument("--read-data", action="store_true", help="Read data files")
    parser.add_argument("--download-videos", action="store_true", help="Download videos")
    parser.add_argument("--export", action="store_true", help="Export to XLSX")

    args = parser.parse_args()

    any_arguments_provided = False

    if args.create_db:
        init_db()
        any_arguments_provided = True

    if args.read_data:
        create_records()
        any_arguments_provided = True

    if args.download_videos:
        retrieve_links()
        retrieve_videos()
        any_arguments_provided = True

    if args.export:
        export_xlsx()
        any_arguments_provided = True        

    if not any_arguments_provided:
        init_db()
        create_records()
        retrieve_links()
        retrieve_videos()
        export_xlsx()

if __name__ == '__main__':
    main()
