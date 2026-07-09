"""Complete database setup script."""

import subprocess
import sys
from pathlib import Path


def create_database_structure():
    """Create complete database structure."""
    print("🚀 Setting up database structure...")

    # Create directories
    db_dir = Path("src/database")
    db_dir.mkdir(parents=True, exist_ok=True)

    # Create __init__.py
    init_file = db_dir / "__init__.py"
    init_file.write_text('"""Database management module."""\n')

    print("✅ Directory structure created")
    return db_dir


def check_postgresql():
    """Check if PostgreSQL is installed and running."""
    print("\n📋 Checking PostgreSQL...")

    try:
        result = subprocess.run(["psql", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PostgreSQL found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        print("❌ PostgreSQL not found in PATH")
        return False

    return False


def create_database():
    """Create travel_planner database."""
    print("\n📋 Creating database...")

    # Check if database exists
    check_cmd = ["psql", "-U", "postgres", "-lqt"]

    try:
        result = subprocess.run(check_cmd, capture_output=True, text=True)

        if "travel_planner" in result.stdout:
            print("ℹ️  Database 'travel_planner' already exists")
            return True

        # Create database
        create_cmd = ["psql", "-U", "postgres", "-c", "CREATE DATABASE travel_planner;"]

        result = subprocess.run(create_cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Database 'travel_planner' created")
            return True
        else:
            print(f"❌ Failed to create database: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def run_schema():
    """Run database schema migrations."""
    print("\n📋 Setting up database schema...")

    migrations_dir = Path("migrations")

    if not migrations_dir.exists():
        print(f"❌ Migrations directory not found: {migrations_dir}")
        return False

    migrations = sorted(list(migrations_dir.glob("*.sql")))
    if not migrations:
        print("❌ No migration files found")
        return False

    for schema_file in migrations:
        print(f"   Executing {schema_file.name}...")
        try:
            cmd = ["psql", "-U", "postgres", "-d", "travel_planner", "-f", str(schema_file)]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"❌ Migration {schema_file.name} failed: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ Error during {schema_file.name}: {e}")
            return False

    print("✅ All database migrations applied successfully")
    return True


def main():
    """Main setup function."""
    print("🚀 DATABASE SETUP SCRIPT")
    print("=" * 60)

    # Step 1: Create directory structure
    db_dir = create_database_structure()

    # Step 2: Check PostgreSQL
    if not check_postgresql():
        print("\n⚠️  Please install PostgreSQL first:")
        print("   https://www.postgresql.org/download/")
        sys.exit(1)

    # Step 3: Create database
    if not create_database():
        print("\n⚠️  Database creation failed")
        sys.exit(1)

    # Step 4: Run schema
    if not run_schema():
        print("\n⚠️  Schema setup failed")
        sys.exit(1)

    # Step 5: Verify
    print("\n" + "=" * 60)
    print("✅ DATABASE SETUP COMPLETE!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Update .env file with database credentials")
    print("2. Run: python check_everything.py")
    print("3. Start app: streamlit run app.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback

        traceback.print_exc()
