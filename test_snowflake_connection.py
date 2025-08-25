#!/usr/bin/env python3
"""
Test Snowflake Connection and List Available Tables
"""

import os
import snowflake.connector
from snowflake.connector import connect

def test_snowflake_connection():
    """Test Snowflake connection and list available tables."""
    try:
        # Get connection parameters from environment
        account = os.environ.get('SNOWFLAKE_ACCOUNT')
        user = os.environ.get('SNOWFLAKE_USER')
        authenticator = os.environ.get('SNOWFLAKE_AUTHENTICATOR', 'externalbrowser')
        warehouse = os.environ.get('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH')
        database = os.environ.get('SNOWFLAKE_DATABASE', 'PROD__US')
        schema = os.environ.get('SNOWFLAKE_SCHEMA', 'DBT_ANALYTICS')
        
        print(f"🔍 Testing connection to: {account}")
        print(f"👤 User: {user}")
        print(f"🏭 Warehouse: {warehouse}")
        print(f"📊 Database: {database}")
        print(f"📋 Schema: {schema}")
        print("-" * 50)
        
        # Connect to Snowflake
        conn = connect(
            account=account,
            user=user,
            authenticator=authenticator,
            warehouse=warehouse,
            database=database,
            schema=schema
        )
        
        cursor = conn.cursor()
        
        # Ensure warehouse is active
        cursor.execute(f"USE WAREHOUSE {warehouse}")
        cursor.execute(f"USE DATABASE {database}")
        cursor.execute(f"USE SCHEMA {schema}")
        
        # Test simple query to verify connection
        cursor.execute("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_WAREHOUSE()")
        connection_info = cursor.fetchone()
        
        print("✅ Snowflake connection successful!")
        print(f"📊 Connected to: {connection_info[0]}.{connection_info[1]}")
        print(f"🏭 Using warehouse: {connection_info[2]}")
        
        # List available tables in the schema
        print("\n📋 Available tables in schema:")
        cursor.execute(f"SHOW TABLES IN {database}.{schema}")
        tables = cursor.fetchall()
        
        if tables:
            for i, table in enumerate(tables[:20]):  # Show first 20 tables
                table_name = table[1]
                print(f"  {i+1:2d}. {table_name}")
            
            if len(tables) > 20:
                print(f"  ... and {len(tables) - 20} more tables")
        else:
            print("  No tables found in this schema")
        
        # Check if the specific table we're trying to use exists
        target_table = "checkout_funnel_v5"
        print(f"\n🔍 Checking if '{target_table}' exists...")
        
        cursor.execute(f"SHOW TABLES LIKE '{target_table}' IN {database}.{schema}")
        target_tables = cursor.fetchall()
        
        if target_tables:
            print(f"✅ Table '{target_table}' found!")
            
            # Get table structure
            print(f"\n📋 Columns in {target_table}:")
            cursor.execute(f"DESCRIBE TABLE {database}.{schema}.{target_table}")
            columns = cursor.fetchall()
            
            for col in columns[:10]:  # Show first 10 columns
                col_name = col[0]
                col_type = col[1]
                print(f"  • {col_name}: {col_type}")
            
            if len(columns) > 10:
                print(f"  ... and {len(columns) - 10} more columns")
        else:
            print(f"❌ Table '{target_table}' not found!")
            
            # Suggest similar tables
            print("\n🔍 Looking for similar tables...")
            cursor.execute(f"SHOW TABLES IN {database}.{schema}")
            all_tables = cursor.fetchall()
            
            similar_tables = [t[1] for t in all_tables if 'checkout' in t[1].lower() or 'funnel' in t[1].lower()]
            if similar_tables:
                print("📋 Similar tables found:")
                for table in similar_tables:
                    print(f"  • {table}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_snowflake_connection()
