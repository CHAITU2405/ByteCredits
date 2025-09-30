# Attendance Portal Feature

## Overview
The Attendance Portal is a new feature added to the ByteCredits admin dashboard that allows teachers and administrators to take attendance using NFC cards. The system supports both built-in mobile NFC readers and external NFC readers.

## Features

### 1. NFC Reader Support
- **Built-in NFC Reader**: Uses the Web NFC API for mobile devices
- **External NFC Reader**: Uses the existing nfcpy library for external USB NFC readers
- Toggle button to switch between reader types

### 2. Attendance Management
- Start/Stop attendance sessions
- Real-time attendance logging
- Duplicate detection (prevents marking the same student twice)
- Subject/Class name input for organization

### 3. Data Storage
- **Excel File Storage**: All attendance data is stored in Excel files (not in database)
- **File Organization**: Files are saved in `static/attendance/` directory
- **Automatic Naming**: Files are named with subject, date, and timestamp

### 4. Data Export
- Download current session as Excel file
- View attendance history
- Download previous attendance files

## How to Use

### For Teachers/Admins:

1. **Access the Portal**:
   - Login as admin or teacher
   - Go to Admin Dashboard
   - Click on "Attendance Portal" card

2. **Start Attendance**:
   - Enter subject/class name
   - Select NFC reader type (Built-in or External)
   - Click "Start Attendance"
   - System will begin scanning for NFC cards

3. **Take Attendance**:
   - Students tap their NFC cards
   - System automatically records name, roll number, email, and timestamp
   - Real-time display of attendance list

4. **Stop Attendance**:
   - Click "Stop Attendance" when done
   - System automatically saves data to Excel file

5. **View/Download**:
   - Use "View Attendance" to see all previous files
   - Use "Download Excel" to download current session
   - Download individual files from attendance history

## Technical Details

### NFC Card Format
NFC cards should contain JSON data with the following structure:
```json
{
    "name": "Student Name",
    "roll_no": "Roll Number",
    "email": "student@email.com"
}
```

### File Structure
```
static/
└── attendance/
    ├── attendance_Mathematics_20250115_143022.xlsx
    ├── attendance_Physics_20250115_150315.xlsx
    └── ...
```

### Excel File Format
Each Excel file contains the following columns:
- Name
- Roll No
- Email
- Time
- Subject
- Date

## API Endpoints

- `GET /read_external_nfc` - Read NFC card using external reader
- `POST /save_attendance` - Save attendance data to Excel file
- `POST /download_attendance` - Download current session as Excel
- `GET /view_attendance_history` - View all attendance files
- `GET /download_attendance_file/<filename>` - Download specific file

## Security
- Only admin and teacher roles can access attendance features
- File downloads are restricted to admin users
- Filename validation prevents directory traversal attacks

## Browser Compatibility
- **Built-in NFC**: Requires Chrome/Edge with Web NFC API support
- **External NFC**: Works with any browser (uses backend polling)

## Dependencies
- pandas (for Excel file creation)
- openpyxl (for Excel file handling)
- nfcpy (for external NFC reader support)

## Installation
```bash
pip install pandas openpyxl
```

The nfcpy library should already be installed as it was part of the original project.
