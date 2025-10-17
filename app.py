import os
from flask import Flask, render_template, session
from utils.db import get_db
from dotenv import load_dotenv

load_dotenv()