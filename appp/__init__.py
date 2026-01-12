from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import timedelta, datetime
from dotenv import load_dotenv
from pathlib import Path
import os

def create_app():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    