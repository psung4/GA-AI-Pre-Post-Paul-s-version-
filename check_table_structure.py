#!/usr/bin/env python3
"""
Check Table Structure of CHECKOUT_FUNNEL_V5
"""

import os
import snowflake.connector
from snowflake.connector import connect

def check_table_structure():
    """Check the structure of CHECKOUT_FUNNEL_V5 table."""
    try:
        # Get connection parameters from environment
        account = os.environ.get('SNOWFLAKE_ACCOUNT')
        user = os.environ.get('SNOWFLAKE_USER')
        authenticator = os.environ.get('SNOWFLAKE_AUTHENTICATOR', 'externalbrowser')
        warehouse = os.environ.get('SNOWFLAKE_WAREHOUSE', 'SHARED')
        
        print(f"🔍 Checking structure of CHECKOUT_FUNNEL_V5 table...")
        print("-" * 50)
        
        # Connect to Snowflake
        conn = connect(
            account=account,
            user=user,
            authenticator=authenticator,
            warehouse=warehouse
        )
        
        cursor = conn.cursor()
        
        # Activate warehouse and use database/schema
        cursor.execute(f"USE WAREHOUSE {warehouse}")
        cursor.execute("USE DATABASE PROD__US")
        cursor.execute("USE SCHEMA DBT_ANALYTICS")
        print("✅ Connected to PROD__US.DBT_ANALYTICS")
        
        # Check if the table exists
        print(f"\n🔍 Checking if CHECKOUT_FUNNEL_V5 exists...")
        cursor.execute("SHOW TABLES LIKE 'CHECKOUT_FUNNEL_V5' IN PROD__US.DBT_ANALYTICS")
        table_exists = cursor.fetchall()
        
        if table_exists:
            print("✅ Table CHECKOUT_FUNNEL_V5 found!")
            
            # Get table structure
            print(f"\n📋 Columns in CHECKOUT_FUNNEL_V5:")
            cursor.execute("DESCRIBE TABLE PROD__US.DBT_ANALYTICS.CHECKOUT_FUNNEL_V5")
            columns = cursor.fetchall()
            
            if columns:
                for i, col in enumerate(columns):
                    col_name = col[0]
                    col_type = col[1]
                    nullable = col[2]
                    default = col[3]
                    print(f"  {i+1:2d}. {col_name:<30} {col_type:<20} {nullable:<8} {default}")
            else:
                print("  No columns found")
            
            # Check if we can query the table
            print(f"\n🔍 Testing a simple query on CHECKOUT_FUNNEL_V5...")
            try:
                cursor.execute("SELECT COUNT(*) FROM PROD__US.DBT_ANALYTICS.CHECKOUT_FUNNEL_V5 LIMIT 1")
                count = cursor.fetchone()
                print(f"✅ Query successful! Table has data.")
            except Exception as e:
                print(f"❌ Query failed: {e}")
            
            # Check for specific columns we need
            print(f"\n🔍 Looking for key columns we need...")
            needed_columns = [
                'checkout_created_dt',
                'merchant_ari', 
                'user_ari',
                'total_amount',
                'is_login_authenticated',
                'is_identity_approved',
                'is_fraud_approved',
                'is_checkout_applied',
                'is_approved',
                'is_confirmed',
                'is_authed',
                'loan_type'
            ]
            
            column_names = [col[0].lower() for col in columns]
            for needed_col in needed_columns:
                if needed_col in column_names:
                    print(f"  ✅ {needed_col}")
                else:
                    print(f"  ❌ {needed_col} - NOT FOUND")
            
        else:
            print("❌ Table CHECKOUT_FUNNEL_V5 not found!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_table_structure()
