-- Renames the habit column that carried a commercial brand name:
--   used_sensodyne -> used_fluoride_toothpaste
--
-- Run this against a DEPLOYED database only. A fresh clone needs nothing: the
-- column is created under its new name by create_db_and_tables() on startup.
--
-- SQLModel's create_all() does not alter existing tables, so without this the
-- application code and the deployed schema disagree and every habit write fails.
--
-- Requires SQLite 3.25+ for RENAME COLUMN (check: sqlite3 --version).
-- Back up the database file before running.
--
--   cp database/oral_health.db database/oral_health.db.bak
--   sqlite3 database/oral_health.db < migration_rename_used_sensodyne.sql
--
-- Verify afterwards:
--   sqlite3 database/oral_health.db "PRAGMA table_info(dailyhabitlog);"
-- used_fluoride_toothpaste should be present and used_sensodyne gone.

BEGIN;

ALTER TABLE dailyhabitlog
    RENAME COLUMN used_sensodyne TO used_fluoride_toothpaste;

COMMIT;
