#!/usr/bin/env bash

# ==============================================================================
# Production PostgreSQL Backup Script
# ==============================================================================
# This script runs pg_dump inside the active app-postgres container, compresses 
# the stream using gzip, saves it to the host filesystem, and cleans up backups 
# older than the retention period.
# ==============================================================================

set -euo pipefail

# Configuration
BACKUP_DIR="${BACKUP_DIR:-/var/backups/postgres}"
RETENTION_DAYS=7
CONTAINER_NAME="app-postgres"
DB_NAME="${POSTGRES_DB:-app_db}"
DB_USER="${POSTGRES_USER:-postgres}"
DATE=$(date +%Y-%m-%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_backup_${DATE}.sql.gz"

echo "[$DATE] Starting database backup for database '$DB_NAME'..."

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# Stream pg_dump output from container directly to compressed file on host
if ! docker exec -t "$CONTAINER_NAME" pg_dump -U "$DB_USER" -d "$DB_NAME" | gzip > "$BACKUP_FILE"; then
    echo "ERROR: Database backup failed!" >&2
    exit 1
fi

echo "Backup file written to: $BACKUP_FILE"

# Clean up older backups
echo "Applying retention policy (deleting files older than $RETENTION_DAYS days)..."
find "$BACKUP_DIR" -name "${DB_NAME}_backup_*.sql.gz" -type f -mtime +"$RETENTION_DAYS" -exec rm -f {} \;

echo "Backup routine completed successfully."
