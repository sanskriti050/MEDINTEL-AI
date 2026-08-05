"""
database.py
───────────
SQLite persistence layer for MedIntel AI.

Creates / manages a local file  →  medintel.db
Three tables:
  • reports       — health report entries (from Report Analyzer + manual log)
  • daily_vitals  — BP, HR, SpO2, temp, weight, water, sleep logs
  • profile       — single-row user health profile

All functions are safe to call at any time:
  - DB + tables are created automatically on first run.
  - No installation required — sqlite3 is part of Python's standard library.
"""

import sqlite3
import json
import os
from datetime import datetime

# DB file lives in the project root
_DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")


# ─────────────────────────────────────────────────────────────────────────────
# CONNECTION HELPER
# ─────────────────────────────────────────────────────────────────────────────

def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row          # rows behave like dicts
    conn.execute("PRAGMA journal_mode=WAL") # safer concurrent writes
    return conn


# ─────────────────────────────────────────────────────────────────────────────
# INITIALISE — call once at app startup
# ─────────────────────────────────────────────────────────────────────────────

def init_db() -> None:
    """Create all tables if they don't already exist."""
    with _get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS reports (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            date           TEXT    NOT NULL,
            report_type    TEXT    NOT NULL,
            score          INTEGER NOT NULL,
            risk           TEXT    NOT NULL,
            abnormal_count INTEGER DEFAULT 0,
            notes          TEXT    DEFAULT '',
            source         TEXT    DEFAULT 'manual',
            filename       TEXT    DEFAULT '',
            added_at       TEXT    NOT NULL,
            hemoglobin     REAL,
            cholesterol    REAL,
            blood_sugar    REAL,
            tsh            REAL,
            creatinine     REAL,
            vitamin_d      REAL
        );

        CREATE TABLE IF NOT EXISTS daily_vitals (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            date       TEXT NOT NULL,
            bp         TEXT,
            heart_rate REAL,
            spo2       REAL,
            temp       REAL,
            weight     REAL,
            water      REAL,
            sleep      REAL
        );

        CREATE TABLE IF NOT EXISTS profile (
            id          INTEGER PRIMARY KEY CHECK (id = 1),
            name        TEXT DEFAULT '',
            age         INTEGER DEFAULT 25,
            gender      TEXT DEFAULT 'Male',
            blood_group TEXT DEFAULT 'A+',
            weight      REAL DEFAULT 70.0,
            height      REAL DEFAULT 170.0,
            conditions  TEXT DEFAULT '',
            allergies   TEXT DEFAULT ''
        );
        """)


# ─────────────────────────────────────────────────────────────────────────────
# REPORTS
# ─────────────────────────────────────────────────────────────────────────────

def save_report(entry: dict) -> None:
    """Insert a report entry. Skips exact duplicates (same filename+date+score)."""
    with _get_conn() as conn:
        # Duplicate check
        existing = conn.execute(
            "SELECT 1 FROM reports WHERE filename=? AND date=? AND score=?",
            (entry.get("filename",""), entry.get("date",""), entry.get("score", 0))
        ).fetchone()
        if existing:
            return

        conn.execute("""
            INSERT INTO reports
              (date, report_type, score, risk, abnormal_count, notes,
               source, filename, added_at,
               hemoglobin, cholesterol, blood_sugar, tsh, creatinine, vitamin_d)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            entry.get("date", ""),
            entry.get("report_type", "General Medical Report"),
            int(entry.get("score", 0)),
            entry.get("risk", "Moderate"),
            int(entry.get("abnormal_count", 0)),
            entry.get("notes", ""),
            entry.get("source", "manual"),
            entry.get("filename", ""),
            entry.get("added_at", datetime.now().isoformat()),
            entry.get("hemoglobin"),
            entry.get("cholesterol"),
            entry.get("blood_sugar"),
            entry.get("tsh"),
            entry.get("creatinine"),
            entry.get("vitamin_d"),
        ))


def load_reports() -> list[dict]:
    """Return all reports ordered by date ascending."""
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM reports ORDER BY date ASC, id ASC"
        ).fetchall()
    return [dict(row) for row in rows]


def delete_last_report() -> None:
    """Delete the most recently added report row."""
    with _get_conn() as conn:
        conn.execute("""
            DELETE FROM reports WHERE id = (SELECT MAX(id) FROM reports)
        """)


# ─────────────────────────────────────────────────────────────────────────────
# DAILY VITALS
# ─────────────────────────────────────────────────────────────────────────────

def save_daily_vitals(entry: dict) -> None:
    """Insert a daily vitals entry."""
    with _get_conn() as conn:
        conn.execute("""
            INSERT INTO daily_vitals
              (date, bp, heart_rate, spo2, temp, weight, water, sleep)
            VALUES (?,?,?,?,?,?,?,?)
        """, (
            entry.get("date", ""),
            entry.get("bp", ""),
            entry.get("heart_rate"),
            entry.get("spo2"),
            entry.get("temp"),
            entry.get("weight"),
            entry.get("water"),
            entry.get("sleep"),
        ))


def load_daily_vitals() -> list[dict]:
    """Return all daily vitals ordered by date ascending."""
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM daily_vitals ORDER BY date ASC, id ASC"
        ).fetchall()
    return [dict(row) for row in rows]


# ─────────────────────────────────────────────────────────────────────────────
# PROFILE
# ─────────────────────────────────────────────────────────────────────────────

def save_profile(profile: dict) -> None:
    """Upsert the single user profile row (id always = 1)."""
    with _get_conn() as conn:
        conn.execute("""
            INSERT INTO profile
              (id, name, age, gender, blood_group, weight, height, conditions, allergies)
            VALUES (1,?,?,?,?,?,?,?,?)
            ON CONFLICT(id) DO UPDATE SET
              name=excluded.name,
              age=excluded.age,
              gender=excluded.gender,
              blood_group=excluded.blood_group,
              weight=excluded.weight,
              height=excluded.height,
              conditions=excluded.conditions,
              allergies=excluded.allergies
        """, (
            profile.get("name", ""),
            int(profile.get("age", 25)),
            profile.get("gender", "Male"),
            profile.get("blood_group", "A+"),
            float(profile.get("weight", 70.0)),
            float(profile.get("height", 170.0)),
            profile.get("conditions", ""),
            profile.get("allergies", ""),
        ))


def load_profile() -> dict:
    """Return the saved profile dict, or sensible defaults if none saved yet."""
    with _get_conn() as conn:
        row = conn.execute("SELECT * FROM profile WHERE id=1").fetchone()
    if row:
        return dict(row)
    return {
        "name": "", "age": 25, "gender": "Male",
        "blood_group": "A+", "weight": 70.0, "height": 170.0,
        "conditions": "", "allergies": ""
    }
