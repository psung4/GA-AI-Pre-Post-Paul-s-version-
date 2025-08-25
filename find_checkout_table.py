#!/usr/bin/env python3
"""
Find Checkout Funnel Table in Snowflake
"""

import os
import snowflake.connector
from snowflake.connector import connect

def find_checkout_table():
    """Find the checkout funnel table in Snowflake."""
    try:
        # Get connection parameters from environment
        account = os.environ.get('SNOWFLAKE_ACCOUNT')
        user = os.environ.get('SNOWFLAKE_USER')
        authenticator = os.environ.get('SNOWFLAKE_AUTHENTICATOR', 'externalbrowser')
        
        print(f"🔍 Searching for checkout funnel table...")
        print("-" * 50)
        
        # Connect to Snowflake
        conn = connect(
            account=account,
            user=user,
            authenticator=authenticator
        )
        
        cursor = conn.cursor()
        
        # Activate a working warehouse
        cursor.execute("USE WAREHOUSE SHARED")
        print("✅ Warehouse SHARED activated")
        
        # Use the database and schema
        cursor.execute("USE DATABASE PROD__US")
        cursor.execute("USE SCHEMA DBT_ANALYTICS")
        print("✅ Database and schema activated")
        
        # Search for tables with 'checkout' in the name
        print("\n🔍 Searching for tables with 'checkout' in the name...")
        cursor.execute("SHOW TABLES IN PROD__US.DBT_ANALYTICS")
        all_tables = cursor.fetchall()
        
        checkout_tables = [t for t in all_tables if 'checkout' in t[1].lower()]
        if checkout_tables:
            print(f"✅ Found {len(checkout_tables)} tables with 'checkout' in the name:")
            for i, table_info in enumerate(checkout_tables):
                table_name = table_info[1]
                print(f"  {i+1:2d}. {table_name}")
        else:
            print("❌ No tables with 'checkout' in the name found")
        
        # Search for tables with 'funnel' in the name
        print("\n🔍 Searching for tables with 'funnel' in the name...")
        funnel_tables = [t for t in all_tables if 'funnel' in t[1].lower()]
        if funnel_tables:
            print(f"✅ Found {len(funnel_tables)} tables with 'funnel' in the name:")
            for i, table_info in enumerate(funnel_tables):
                table_name = table_info[1]
                print(f"  {i+1:2d}. {table_name}")
        else:
            print("❌ No tables with 'funnel' in the name found")
        
        # Search for tables with 'conversion' in the name
        print("\n🔍 Searching for tables with 'conversion' in the name...")
        conversion_tables = [t for t in all_tables if 'conversion' in t[1].lower()]
        if conversion_tables:
            print(f"✅ Found {len(conversion_tables)} tables with 'conversion' in the name:")
            for i, table_info in enumerate(conversion_tables):
                table_name = table_info[1]
                print(f"  {i+1:2d}. {table_name}")
        else:
            print("❌ No tables with 'conversion' in the name found")
        
        # List all tables to see what's available
        print("\n📋 All tables in DBT_ANALYTICS (showing first 50):")
        cursor.execute("SHOW TABLES IN PROD__US.DBT_ANALYTICS")
        all_tables = cursor.fetchall()
        
        if all_tables:
            for i, table_info in enumerate(all_tables[:50]):
                table_name = table_info[1]
                print(f"  {i+1:2d}. {table_name}")
            
            if len(all_tables) > 50:
                print(f"  ... and {len(all_tables) - 50} more tables")
        else:
            print("  No tables found")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    find_checkout_table()
