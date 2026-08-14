CREATE TABLE IF NOT EXISTS users (
 id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL,
 password_hash TEXT NOT NULL, full_name TEXT NOT NULL, role TEXT NOT NULL, is_active INTEGER DEFAULT 1);
CREATE TABLE IF NOT EXISTS assets (
 id INTEGER PRIMARY KEY, asset_code TEXT UNIQUE NOT NULL, asset_name TEXT NOT NULL,
 road_name TEXT NOT NULL, latitude REAL NOT NULL, longitude REAL NOT NULL,
 area_zone TEXT NOT NULL, sidewalk_width_m REAL NOT NULL, usable_area_m2 REAL NOT NULL,
 management_unit TEXT, status TEXT NOT NULL, allowed_purposes TEXT, notes TEXT);
CREATE TABLE IF NOT EXISTS applications (
 id INTEGER PRIMARY KEY AUTOINCREMENT, application_code TEXT UNIQUE NOT NULL,
 applicant_user_id INTEGER NOT NULL, asset_id INTEGER NOT NULL, applicant_name TEXT NOT NULL,
 phone_number TEXT NOT NULL, purpose_code TEXT NOT NULL, requested_area_m2 REAL NOT NULL,
 start_date TEXT NOT NULL, end_date TEXT NOT NULL, description TEXT, has_image INTEGER DEFAULT 0,
 status TEXT NOT NULL, submitted_at TEXT NOT NULL, officer_note TEXT, ai_result_json TEXT,
 fee_amount REAL DEFAULT 0, permit_code TEXT);
CREATE TABLE IF NOT EXISTS activity_logs (
 id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, application_code TEXT,
 action TEXT NOT NULL, created_at TEXT NOT NULL);
