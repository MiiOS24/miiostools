import os
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to read data from Google Sheets
def read_from_google_sheets(sheet_id, sheet_name):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')  # Load from .env

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=f"{sheet_name}!A:D").execute()
    values = result.get('values', [])

    if not values:
        print('Keine Daten gefunden.')
        return pd.DataFrame()

    df = pd.DataFrame(values[1:], columns=values[0])
    return df

# Function to convert German number format to float
def german_to_float(value):
    if pd.isna(value):
        return np.nan
    return float(str(value).replace(',', '.'))

# Function to process working hours data
def process_working_hours(df):
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y', errors='coerce')
    df['started'] = df['started'].apply(german_to_float)
    df['stopped'] = df['stopped'].apply(german_to_float)
    df['hours_worked'] = df['stopped'] - df['started']
    
    # Remove rows with invalid data or working hours
    df = df.dropna(subset=['date', 'started', 'stopped', 'hours_worked'])
    df = df[df['hours_worked'] >= 0]
    
    df['week'] = df['date'].dt.isocalendar().week.astype(int)
    df['year'] = df['date'].dt.isocalendar().year.astype(int)
    
    # Exclude the current week
    current_week = datetime.now().isocalendar().week
    current_year = datetime.now().isocalendar().year
    
    df = df[~((df['week'] == current_week) & (df['year'] == current_year))]
    
    weekly_hours = df.groupby(['year', 'week'])['hours_worked'].sum().reset_index()
    
    # Calculate extra or deficit hours
    weekly_hours['extra_hours'] = weekly_hours['hours_worked'] - 20
    
    return weekly_hours

# Function to plot weekly worked hours as a line chart
def plot_weekly_hours(weekly_hours):
    fig, ax = plt.subplots()
    weeks = weekly_hours['week'].astype(int)
    hours = weekly_hours['hours_worked']

    ax.plot(weeks, hours, color='blue', marker='o', linestyle='-', alpha=0.7)
    
    # Add a horizontal red line for contract hours
    contracted_hours = 20  # Contract hours per week
    ax.axhline(y=contracted_hours, color='red', linestyle='--', linewidth=2)
    ax.text(weeks.max() + 1, contracted_hours, '20h', color='red', verticalalignment='center')
    
    ax.set_xlabel('Woche')
    ax.set_ylabel('Gearbeitete Stunden')
    ax.set_title('Gearbeitete Stunden pro Woche')
    
    ax.set_xticks(weeks)
    ax.set_xticklabels(weeks)
    
    st.pyplot(fig)

# Function to plot extra or deficit hours per week
def plot_extra_hours(weekly_hours):
    fig, ax = plt.subplots()
    weeks = weekly_hours['week'].astype(int)
    extra_hours = weekly_hours['extra_hours']

    colors = ['red' if eh > 0 else 'grey' for eh in extra_hours]

    ax.bar(weeks, extra_hours, color=colors, alpha=0.7)
    
    ax.set_xlabel('Woche')
    ax.set_ylabel('Über-/Minusstunden')
    ax.set_title('Über-/Minusstunden pro Woche')
    
    ax.set_xticks(weeks)
    ax.set_xticklabels(weeks)
    
    st.pyplot(fig)

# Page function for Streamlit app
def maddehours_page():
    st.title("Arbeitszeitanalyse Madde")

    # Google Sheets Details
    SHEET_ID = os.getenv('SHEET_ID')
    SHEET_NAME = os.getenv('SHEET_NAME')

    # Read data from Google Sheets
    df = read_from_google_sheets(SHEET_ID, SHEET_NAME)

    if not df.empty:
        st.write("Daten erfolgreich geladen!")

        # Process and display weekly worked hours
        weekly_hours = process_working_hours(df)
        st.subheader("Wöchentlich gearbeitete Stunden")
        plot_weekly_hours(weekly_hours)
        
        # Display extra or deficit hours per week
        st.subheader("Über-/Minusstunden pro Woche")
        plot_extra_hours(weekly_hours)
        
        # Calculate and display statistics
        total_extra_hours = weekly_hours['extra_hours'].sum()
        total_extra_days = total_extra_hours / 8  # Assuming 8-hour workday
        total_extra_weeks = total_extra_hours / 20  # Assuming 20-hour workweek
        
        st.subheader("Statistiken")
        st.write(f"Gesamte Überstunden: {total_extra_hours:.2f}")
        st.write(f"Gesamte Überstunden in Tagen: {total_extra_days:.2f} Tage")
        st.write(f"Gesamte Überstunden in Wochen: {total_extra_weeks:.2f} Wochen")
        
        # Display processed data
        st.subheader("Verarbeitete Daten")
        st.write(weekly_hours)
    else:
        st.error("Keine Daten verfügbar. Bitte überprüfen Sie Ihre Google Sheets-Verbindung.")
