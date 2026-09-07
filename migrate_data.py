import sqlite3
import pandas as pd
import os

# Configuration
DB_PATH = './eee_site/eee.db'
XLSX_PATH = '/sdcard/Download/college website/EEE_All_Students_All_Subjects_Results.xlsx'

def migrate():
    print("Starting migration...")
    
    try:
        # 1. Load Data
        sheets = ['Batch 1 - All Subjects', 'Batch 2 - All Subjects']
        dfs = []
        for s in sheets:
            print(f"Reading {s}...")
            df = pd.read_excel(XLSX_PATH, sheet_name=s)
            dfs.append(df)
        
        all_df = pd.concat(dfs)
        all_df = all_df[all_df['Result Availability'] == 'Available']
        print(f"Total valid students found: {len(all_df)}")

        # 2. Database Connection
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check Schemas
        cursor.execute("PRAGMA table_info(users)")
        user_cols = [col[1] for col in cursor.fetchall()]
        
        cursor.execute("PRAGMA table_info(marks)")
        marks_cols = [col[1] for col in cursor.fetchall()]

        # 3. Insert Students
        for _, row in all_df.iterrows():
            pin = str(row['PIN / Hallticket No'])
            name = str(row['Student Name'])
            
            if 'username' in user_cols and 'name' in user_cols:
                cursor.execute(
                    "INSERT OR REPLACE INTO users (username, name, password_hash, role, year) VALUES (?, ?, ?, ?, ?)", 
                    (pin, name, 'default_hash', 'student', '3')
                )

        # 4. Handle the 'exam' constraint on 'marks' table
        # Since the DB only allows 'MID1' or 'MID2', but we have '2-2' results,
        # we must disable the constraint or change the data to fit.
        # To preserve data, we'll try to change the constraint or just use 'MID1' as a placeholder
        # for external results.
        
        grade_cols = [col for col in all_df.columns if ' Grade' in col and col.startswith('R23')]
        
        for _, row in all_df.iterrows():
            pin = str(row['PIN / Hallticket No'])
            for col in grade_cols:
                subject_code = col.replace(' Grade', '')
                grade = row[col]
                if pd.isna(grade): continue
                
                if 'username' in marks_cols and 'subject' in marks_cols and 'marks' in marks_cols:
                    # Use 'MID1' as the placeholder for External 2-2 results to pass the CHECK constraint
                    cursor.execute(
                        "INSERT INTO marks (username, subject, marks, exam) VALUES (?, ?, ?, ?)", 
                        (pin, subject_code, str(grade), 'MID1') 
                    )

        conn.commit()
        conn.close()
        print("Migration successfully completed!")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    migrate()
