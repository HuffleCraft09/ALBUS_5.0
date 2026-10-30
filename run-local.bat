@echo off
title ALBUS 2.0
if not exist .venv (
  py -m venv .venv
)
call .venv\Scripts\activate
python -m pip install -r requirements.txt
if not exist .env (
  copy .env.example .env
  echo.
  echo Created .env. Edit it with your OpenAI API key and ALBUS token.
  pause
  exit /b
)
python server.py
pause
