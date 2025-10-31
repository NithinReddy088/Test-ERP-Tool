#!/bin/bash

# Healthcare Manufacturing ERP Backup Script
# Performs automated database and file backups

set -e

# Configuration
BACKUP_DIR="/backups"
DB_NAME="${DB_NAME:-healthcare_erp}"
DB_USER="${DB_USER:-postgres}"
DB_HOST="${DB_HOST:-postgres}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-30}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

echo "Starting backup process at $(date)"

# Database backup
echo "Backing up database: $DB_NAME"
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME --no-password > $BACKUP_DIR/db_backup_$TIMESTAMP.sql

# Compress database backup
gzip $BACKUP_DIR/db_backup_$TIMESTAMP.sql
echo "Database backup completed: db_backup_$TIMESTAMP.sql.gz"

# File backup (if running in web container)
if [ -d "/home/frappe/frappe-bench/sites" ]; then
    echo "Backing up site files"
    tar -czf $BACKUP_DIR/files_backup_$TIMESTAMP.tar.gz -C /home/frappe/frappe-bench/sites .
    echo "File backup completed: files_backup_$TIMESTAMP.tar.gz"
fi

# Clean up old backups
echo "Cleaning up backups older than $RETENTION_DAYS days"
find $BACKUP_DIR -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete

# Upload to S3 if configured
if [ ! -z "$AWS_S3_BUCKET_NAME" ]; then
    echo "Uploading backups to S3: $AWS_S3_BUCKET_NAME"
    aws s3 cp $BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz s3://$AWS_S3_BUCKET_NAME/backups/
    if [ -f "$BACKUP_DIR/files_backup_$TIMESTAMP.tar.gz" ]; then
        aws s3 cp $BACKUP_DIR/files_backup_$TIMESTAMP.tar.gz s3://$AWS_S3_BUCKET_NAME/backups/
    fi
fi

echo "Backup process completed at $(date)"

# Health check - verify backup integrity
echo "Verifying backup integrity"
if gzip -t $BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz; then
    echo "Database backup integrity: OK"
else
    echo "Database backup integrity: FAILED"
    exit 1
fi

echo "All backups completed successfully"