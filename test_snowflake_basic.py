#!/usr/bin/env python3
"""
Basic Snowflake Connection Test
"""

import os
import snowflake.connector
from snowflake.connector import connect

def test_basic_connection():
    """Test basic Snowflake connection without specifying database/schema."""
    try:
        # Get connection parameters from environment
        account = os.environ.get('SNOWFLAKE_ACCOUNT')
        user = os.environ.get('SNOWFLAKE_USER')
        authenticator = os.environ.get('SNOWFLAKE_AUTHENTICATOR', 'externalbrowser')
        warehouse = os.environ.get('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH')
        
        print(f"🔍 Testing connection to: {account}")
        print(f"👤 User: {user}")
        print(f"🏭 Warehouse: {warehouse}")
        print("-" * 50)
        
        # Connect to Snowflake without specifying database/schema
        conn = connect(
            account=account,
            user=user,
            authenticator=authenticator,
            warehouse=warehouse
        )
        
        cursor = conn.cursor()
        
        # Test basic connection
        print("🔄 Testing basic connection...")
        cursor.execute("SELECT CURRENT_ACCOUNT(), CURRENT_USER(), CURRENT_WAREHOUSE()")
        basic_info = cursor.fetchone()
        
        print("✅ Basic connection successful!")
        print(f"🏢 Account: {basic_info[0]}")
        print(f"👤 User: {basic_info[1]}")
        print(f"🏭 Warehouse: {basic_info[2]}")
        
        # List available warehouses with more detail
        print("\n🏭 Available warehouses:")
        cursor.execute("SHOW WAREHOUSES")
        warehouses = cursor.fetchall()
        
        if warehouses:
            print("  Format: [Name, State, Size, Min_Clusters, Max_Clusters, Started_Clusters, Running_Clusters, Queued_Clusters, Other]")
            for i, warehouse_info in enumerate(warehouses[:10]):
                warehouse_name = warehouse_info[0]  # First column is the name
                warehouse_state = warehouse_info[1]  # Second column is the state
                warehouse_size = warehouse_info[2]  # Third column is the size
                print(f"  {i+1:2d}. {warehouse_name} - {warehouse_state} ({warehouse_size})")
        else:
            print("  No warehouses found")
        
        # List available databases
        print("\n📊 Available databases:")
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        
        if databases:
            for i, db_info in enumerate(databases[:10]):
                db_name = db_info[1]
                db_owner = db_info[3]
                print(f"  {i+1:2d}. {db_name} (Owner: {db_owner})")
        else:
            print("  No databases found")
        
        # Try to use a warehouse
        print(f"\n🔄 Trying to activate a warehouse...")
        if warehouses:
            # Try the first available warehouse
            first_warehouse = warehouses[0][0]  # First column is the name
            print(f"🔄 Trying to use warehouse: {first_warehouse}")
            try:
                cursor.execute(f"USE WAREHOUSE {first_warehouse}")
                print(f"✅ Warehouse {first_warehouse} activated successfully!")
                
                # Now try to use the PROD__US database
                print(f"\n🔄 Trying to use database: PROD__US")
                try:
                    cursor.execute("USE DATABASE PROD__US")
                    print("✅ Database PROD__US activated successfully!")
                    
                    # List schemas in PROD__US
                    print("\n📋 Available schemas in PROD__US:")
                    cursor.execute("SHOW SCHEMAS IN PROD__US")
                    schemas = cursor.fetchall()
                    
                    if schemas:
                        for i, schema_info in enumerate(schemas[:10]):
                            schema_name = schema_info[1]
                            print(f"  {i+1:2d}. {schema_name}")
                    else:
                        print("  No schemas found")
                    
                    # Try to use DBT_ANALYTICS schema
                    print(f"\n🔄 Trying to use schema: DBT_ANALYTICS")
                    try:
                        cursor.execute("USE SCHEMA DBT_ANALYTICS")
                        print("✅ Schema DBT_ANALYTICS activated successfully!")
                        
                        # List tables in the schema
                        print("\n📋 Available tables in DBT_ANALYTICS:")
                        cursor.execute("SHOW TABLES IN PROD__US.DBT_ANALYTICS")
                        tables = cursor.fetchall()
                        
                        if tables:
                            for i, table_info in enumerate(tables[:10]):
                                table_name = table_info[1]
                                print(f"  {i+1:2d}. {table_name}")
                        else:
                            print("  No tables found")
                            
                    except Exception as e:
                        print(f"❌ Failed to use schema DBT_ANALYTICS: {e}")
                        
                except Exception as e:
                    print(f"❌ Failed to use database PROD__US: {e}")
                    
            except Exception as e:
                print(f"❌ Failed to activate warehouse {first_warehouse}: {e}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_basic_connection()
