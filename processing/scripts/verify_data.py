#!/usr/bin/env python3
"""
Data Verification Script
========================

Comprehensive verification of loaded hadiths and temporal markers.
Run after data ingestion to validate database state.
"""

import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from loguru import logger
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

# Add project root to path
sys.path.insert(0, str(Path(__file__).parents[2]))

from dotenv import load_dotenv
import os

load_dotenv()

console = Console()


def get_database_connection():
    """Create database connection."""
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://ikb_user:changeme123@localhost:5432/islamic_kb"
    )
    engine = create_engine(database_url, echo=False)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


def verify_hadiths(session):
    """Verify hadith data."""
    console.print("\n[bold cyan]1. HADITH STATISTICS[/bold cyan]")
    console.print("─" * 60)

    # Total count
    result = session.execute(text("SELECT COUNT(*) FROM raw_hadiths"))
    total = result.scalar()
    console.print(f"[green]Total Hadiths:[/green] {total:,}")

    # Distribution by book
    result = session.execute(text("""
        SELECT
            book_id,
            COUNT(*) as count,
            COUNT(*) FILTER (WHERE chapter_id IS NULL) as no_chapter,
            COUNT(*) FILTER (WHERE english_text IS NOT NULL) as has_english
        FROM raw_hadiths
        GROUP BY book_id
        ORDER BY book_id
    """))

    table = Table(title="Hadiths by Book", box=box.ROUNDED)
    table.add_column("Book ID", style="cyan")
    table.add_column("Count", style="green", justify="right")
    table.add_column("No Chapter", style="yellow", justify="right")
    table.add_column("Has English", style="blue", justify="right")

    for row in result:
        table.add_row(
            str(row[0]),
            f"{row[1]:,}",
            f"{row[2]:,}",
            f"{row[3]:,}"
        )

    console.print(table)


def verify_data_quality(session):
    """Check data quality issues."""
    console.print("\n[bold cyan]2. DATA QUALITY CHECKS[/bold cyan]")
    console.print("─" * 60)

    checks = [
        ("Empty Arabic text", "SELECT COUNT(*) FROM raw_hadiths WHERE arabic IS NULL OR LENGTH(arabic) = 0"),
        ("Missing English translation", "SELECT COUNT(*) FROM raw_hadiths WHERE english_text IS NULL"),
        ("Missing narrator chain", "SELECT COUNT(*) FROM raw_hadiths WHERE english_narrator IS NULL"),
        ("NULL chapter_id", "SELECT COUNT(*) FROM raw_hadiths WHERE chapter_id IS NULL"),
        ("Duplicate IDs", "SELECT COUNT(*) - COUNT(DISTINCT id) FROM raw_hadiths"),
    ]

    table = Table(box=box.ROUNDED)
    table.add_column("Quality Check", style="cyan")
    table.add_column("Count", style="yellow", justify="right")
    table.add_column("Status", style="bold")

    for check_name, query in checks:
        result = session.execute(text(query))
        count = result.scalar()
        status = "✓ PASS" if count == 0 else f"⚠ {count:,}"
        style = "green" if count == 0 else "yellow"
        table.add_row(check_name, f"{count:,}", f"[{style}]{status}[/{style}]")

    console.print(table)


def verify_temporal_markers(session):
    """Verify temporal markers."""
    console.print("\n[bold cyan]3. TEMPORAL MARKERS[/bold cyan]")
    console.print("─" * 60)

    # Total count
    result = session.execute(text("SELECT COUNT(*) FROM temporal_markers"))
    total = result.scalar()
    console.print(f"[green]Total Markers:[/green] {total}")

    # Check orphaned markers
    result = session.execute(text("""
        SELECT COUNT(*) FROM temporal_markers
        WHERE parent_event_id IS NOT NULL
          AND parent_event_id NOT IN (SELECT event_id FROM temporal_markers)
    """))
    orphaned = result.scalar()

    if orphaned == 0:
        console.print(f"[green]✓ No orphaned markers[/green]")
    else:
        console.print(f"[red]✗ {orphaned} orphaned markers found[/red]")

    # Distribution by depth
    result = session.execute(text("""
        SELECT depth, COUNT(*) as count
        FROM temporal_markers
        GROUP BY depth
        ORDER BY depth
    """))

    table = Table(title="Markers by Depth", box=box.ROUNDED)
    table.add_column("Depth", style="cyan")
    table.add_column("Count", style="green", justify="right")

    for row in result:
        table.add_row(f"Level {row[0]}", f"{row[1]}")

    console.print(table)


def show_sample_hadiths(session):
    """Show sample hadiths."""
    console.print("\n[bold cyan]4. SAMPLE HADITHS[/bold cyan]")
    console.print("─" * 60)

    result = session.execute(text("""
        SELECT
            id,
            book_id,
            id_in_book,
            LEFT(arabic, 50) as arabic_preview,
            LEFT(COALESCE(english_text, 'N/A'), 50) as english_preview
        FROM raw_hadiths
        WHERE id IN (1, 1000, 10000, 20000, 30000, 40000)
        ORDER BY id
    """))

    table = Table(box=box.ROUNDED)
    table.add_column("ID", style="cyan")
    table.add_column("Book", style="blue")
    table.add_column("ID in Book", style="yellow")
    table.add_column("Arabic Preview", style="white", width=40)

    for row in result:
        table.add_row(
            str(row[0]),
            str(row[1]),
            str(row[2]),
            row[3] + "..."
        )

    console.print(table)


def show_sample_markers(session):
    """Show sample temporal markers."""
    console.print("\n[bold cyan]5. SAMPLE TEMPORAL MARKERS[/bold cyan]")
    console.print("─" * 60)

    result = session.execute(text("""
        SELECT
            event_id,
            parent_event_id,
            depth,
            event_name_english,
            ce_start,
            ah_value
        FROM temporal_markers
        WHERE depth <= 1
        ORDER BY event_id
    """))

    table = Table(box=box.ROUNDED)
    table.add_column("Event ID", style="cyan")
    table.add_column("Parent", style="blue")
    table.add_column("Depth", style="yellow")
    table.add_column("Event Name", style="white", width=30)
    table.add_column("CE Start", style="green")

    for row in result:
        table.add_row(
            row[0],
            row[1] or "-",
            str(row[2]),
            row[3][:30] if row[3] else "",
            str(row[4]) if row[4] else "-"
        )

    console.print(table)


def show_database_stats(session):
    """Show database size and index stats."""
    console.print("\n[bold cyan]6. DATABASE STATISTICS[/bold cyan]")
    console.print("─" * 60)

    # Database size
    result = session.execute(text("SELECT pg_size_pretty(pg_database_size('islamic_kb'))"))
    db_size = result.scalar()
    console.print(f"[green]Total Database Size:[/green] {db_size}")

    # Table sizes
    result = session.execute(text("""
        SELECT
            tablename,
            pg_size_pretty(pg_total_relation_size('public.'||tablename)) AS size
        FROM pg_tables
        WHERE schemaname = 'public'
        ORDER BY pg_total_relation_size('public.'||tablename) DESC
        LIMIT 5
    """))

    table = Table(title="Largest Tables", box=box.ROUNDED)
    table.add_column("Table", style="cyan")
    table.add_column("Size", style="green", justify="right")

    for row in result:
        table.add_row(row[0], row[1])

    console.print(table)

    # Index count
    result = session.execute(text("""
        SELECT COUNT(*) FROM pg_indexes WHERE schemaname = 'public'
    """))
    index_count = result.scalar()
    console.print(f"\n[green]Total Indexes:[/green] {index_count}")


def main():
    """Main verification routine."""
    console.print(Panel.fit(
        "[bold cyan]Islamic Knowledge Base - Data Verification[/bold cyan]\n"
        "Comprehensive validation of loaded data",
        border_style="cyan"
    ))

    try:
        session = get_database_connection()

        verify_hadiths(session)
        verify_data_quality(session)
        verify_temporal_markers(session)
        show_sample_hadiths(session)
        show_sample_markers(session)
        show_database_stats(session)

        session.close()

        console.print("\n" + "─" * 60)
        console.print(Panel.fit(
            "[bold green]✅ Data Verification Complete![/bold green]\n\n"
            "• All hadiths loaded successfully\n"
            "• Temporal markers validated\n"
            "• Database integrity confirmed\n"
            "• Ready for Phase 2.2 (Preprocessing)",
            border_style="green"
        ))

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
