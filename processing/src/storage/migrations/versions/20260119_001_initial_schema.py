"""Initial schema: 7 core tables for IPKSA hadith processing

Revision ID: 001_initial
Revises:
Create Date: 2026-01-19

Tables:
1. raw_hadiths - Immutable source data (50,884 rows)
2. preprocessed_hadiths - Normalized text, parsed isnad
3. temporal_markers - Prophetic era events reference (54 events)
4. pcap_assignments - PCAP temporal assignments with versioning
5. hmsts_tags - HMSTS semantic tags with versioning
6. hadith_links - Cross-references between hadiths
7. validation_results - Validation outcomes
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create all 7 core tables with indexes and constraints."""

    # ========================================================================
    # TABLE 1: raw_hadiths - Immutable source data
    # ========================================================================
    op.create_table(
        'raw_hadiths',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_in_book', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('chapter_id', sa.Integer(), nullable=False),
        sa.Column('arabic', sa.Text(), nullable=False),
        sa.Column('english_narrator', sa.Text(), nullable=True),
        sa.Column('english_text', sa.Text(), nullable=True),
        sa.Column('book_name_arabic', sa.String(255), nullable=True),
        sa.Column('book_name_english', sa.String(255), nullable=True),
        sa.Column('chapter_name_arabic', sa.Text(), nullable=True),
        sa.Column('chapter_name_english', sa.Text(), nullable=True),
        sa.Column('source_file', sa.String(500), nullable=True),
        sa.Column('loaded_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('book_id', 'id_in_book', name='unique_hadith_in_book')
    )

    # Indexes for raw_hadiths
    op.create_index('idx_raw_hadiths_book', 'raw_hadiths', ['book_id'])
    op.create_index('idx_raw_hadiths_chapter', 'raw_hadiths', ['chapter_id'])
    op.create_index('idx_raw_hadiths_book_chapter', 'raw_hadiths', ['book_id', 'chapter_id'])
    op.execute("CREATE INDEX idx_raw_hadiths_arabic_fts ON raw_hadiths USING gin(to_tsvector('arabic', arabic))")
    op.execute("CREATE INDEX idx_raw_hadiths_english_fts ON raw_hadiths USING gin(to_tsvector('english', COALESCE(english_text, '')))")

    # ========================================================================
    # TABLE 2: preprocessed_hadiths - Normalized text, parsed isnad
    # ========================================================================
    op.create_table(
        'preprocessed_hadiths',
        sa.Column('hadith_id', sa.Integer(), nullable=False),
        sa.Column('arabic_normalized', sa.Text(), nullable=True),
        sa.Column('english_normalized', sa.Text(), nullable=True),
        sa.Column('isnad_chain', postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column('isnad_generation', sa.Integer(), nullable=True),
        sa.Column('explicit_temporal_references', postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column('explicit_person_references', postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column('text_length_arabic', sa.Integer(), nullable=True),
        sa.Column('text_length_english', sa.Integer(), nullable=True),
        sa.Column('has_explicit_date', sa.Boolean(), server_default=sa.text('FALSE'), nullable=True),
        sa.Column('processed_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('preprocessing_version', sa.String(20), server_default=sa.text("'1.0'"), nullable=True),
        sa.PrimaryKeyConstraint('hadith_id'),
        sa.ForeignKeyConstraint(['hadith_id'], ['raw_hadiths.id'], ondelete='CASCADE')
    )

    # Indexes for preprocessed_hadiths
    op.create_index('idx_preprocessed_generation', 'preprocessed_hadiths', ['isnad_generation'])
    op.create_index('idx_preprocessed_has_date', 'preprocessed_hadiths', ['has_explicit_date'],
                    postgresql_where=sa.text('has_explicit_date = TRUE'))

    # ========================================================================
    # TABLE 3: temporal_markers - Prophetic era events reference
    # ========================================================================
    op.create_table(
        'temporal_markers',
        sa.Column('event_id', sa.String(20), nullable=False),
        sa.Column('parent_event_id', sa.String(20), nullable=True),
        sa.Column('depth', sa.Integer(), nullable=False),
        sa.Column('era_category', sa.String(10), nullable=True),
        sa.Column('ce_start', sa.Date(), nullable=True),
        sa.Column('ce_end', sa.Date(), nullable=True),
        sa.Column('ah_value', sa.String(50), nullable=True),
        sa.Column('event_name_english', sa.String(255), nullable=False),
        sa.Column('event_name_arabic', sa.String(255), nullable=True),
        sa.Column('location', sa.String(255), nullable=True),
        sa.Column('significance', sa.Text(), nullable=True),
        sa.Column('certainty_date', sa.String(10), nullable=True),
        sa.Column('certainty_event', sa.String(10), nullable=True),
        sa.Column('source_tradition', sa.String(255), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('loaded_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('event_id'),
        sa.ForeignKeyConstraint(['parent_event_id'], ['temporal_markers.event_id'])
    )

    # Indexes for temporal_markers
    op.create_index('idx_temporal_era', 'temporal_markers', ['era_category'])
    op.create_index('idx_temporal_dates', 'temporal_markers', ['ce_start', 'ce_end'])

    # ========================================================================
    # TABLE 4: pcap_assignments - PCAP temporal assignments
    # ========================================================================
    op.create_table(
        'pcap_assignments',
        sa.Column('id', sa.Integer(), sa.Sequence('pcap_assignments_id_seq'), nullable=False),
        sa.Column('hadith_id', sa.Integer(), nullable=False),
        sa.Column('version', sa.String(20), server_default=sa.text("'v1.0'"), nullable=False),
        sa.Column('era_id', sa.String(20), nullable=False),
        sa.Column('sub_era_id', sa.String(20), nullable=True),
        sa.Column('event_window_id', sa.String(20), nullable=True),
        sa.Column('earliest_ah', sa.Numeric(6, 2), nullable=False),
        sa.Column('latest_ah', sa.Numeric(6, 2), nullable=False),
        sa.Column('earliest_ce', sa.Date(), nullable=True),
        sa.Column('latest_ce', sa.Date(), nullable=True),
        sa.Column('anchor_before', postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column('anchor_after', postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column('evidence_type', sa.String(50), nullable=False),
        sa.Column('posterior_confidence', sa.Numeric(4, 3), nullable=False),
        sa.Column('reasoning', sa.Text(), nullable=False),
        sa.Column('llm_model', sa.String(100), nullable=True),
        sa.Column('llm_cost_usd', sa.Numeric(8, 6), nullable=True),
        sa.Column('processing_duration_ms', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['hadith_id'], ['raw_hadiths.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('hadith_id', 'version', name='unique_pcap_per_version'),
        sa.CheckConstraint('earliest_ah <= latest_ah', name='check_ah_order'),
        sa.CheckConstraint('posterior_confidence >= 0 AND posterior_confidence <= 1', name='check_confidence_range'),
        sa.CheckConstraint(
            "evidence_type IN ('explicit_text', 'explicit_event', 'isnad_generation', 'sirah_alignment', 'contextual_order', 'speculative')",
            name='check_evidence_type'
        )
    )

    # Indexes for pcap_assignments
    op.create_index('idx_pcap_hadith_version', 'pcap_assignments', ['hadith_id', 'version'])
    op.create_index('idx_pcap_era', 'pcap_assignments', ['era_id', 'version'])
    op.create_index('idx_pcap_confidence', 'pcap_assignments', ['posterior_confidence', 'version'])
    op.create_index('idx_pcap_date_range', 'pcap_assignments', ['earliest_ah', 'latest_ah', 'version'])
    op.execute("CREATE INDEX idx_pcap_anchors ON pcap_assignments USING gin(anchor_before, anchor_after)")

    # ========================================================================
    # TABLE 5: hmsts_tags - HMSTS semantic tags
    # ========================================================================
    op.create_table(
        'hmsts_tags',
        sa.Column('id', sa.Integer(), sa.Sequence('hmsts_tags_id_seq'), nullable=False),
        sa.Column('hadith_id', sa.Integer(), nullable=False),
        sa.Column('version', sa.String(20), server_default=sa.text("'v1.0'"), nullable=False),
        sa.Column('layer0_speaker', sa.String(255), nullable=True),
        sa.Column('layer0_addressee', sa.String(255), nullable=True),
        sa.Column('layer0_verb_type', sa.String(100), nullable=True),
        sa.Column('layer0_modality', sa.String(50), nullable=True),
        sa.Column('layer1_categories', postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column('layer2_role', sa.String(50), nullable=False),
        sa.Column('layer3_axis_a', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('layer3_axis_b', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('layer4_vectors', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('llm_model', sa.String(100), nullable=True),
        sa.Column('llm_cost_usd', sa.Numeric(8, 6), nullable=True),
        sa.Column('processing_duration_ms', sa.Integer(), nullable=True),
        sa.Column('semantic_completeness_score', sa.Numeric(4, 3), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['hadith_id'], ['raw_hadiths.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('hadith_id', 'version', name='unique_hmsts_per_version'),
        sa.CheckConstraint(
            "layer0_modality IN ('obligatory', 'recommended', 'permitted', 'discouraged', 'forbidden', 'informative')",
            name='check_modality'
        ),
        sa.CheckConstraint(
            "layer2_role IN ('Normative', 'Descriptive', 'Explanatory', 'Corrective', 'Exemplary', 'Prophetic State', 'Divine Address', 'Divine Attribute')",
            name='check_role'
        )
    )

    # Indexes for hmsts_tags
    op.create_index('idx_hmsts_hadith_version', 'hmsts_tags', ['hadith_id', 'version'])
    op.create_index('idx_hmsts_modality', 'hmsts_tags', ['layer0_modality', 'version'])
    op.create_index('idx_hmsts_role', 'hmsts_tags', ['layer2_role', 'version'])
    op.execute("CREATE INDEX idx_hmsts_categories ON hmsts_tags USING gin(layer1_categories)")
    op.execute("CREATE INDEX idx_hmsts_layer3_a ON hmsts_tags USING gin(layer3_axis_a)")
    op.execute("CREATE INDEX idx_hmsts_layer3_b ON hmsts_tags USING gin(layer3_axis_b)")
    op.execute("CREATE INDEX idx_hmsts_layer4 ON hmsts_tags USING gin(layer4_vectors)")

    # ========================================================================
    # TABLE 6: hadith_links - Cross-references between hadiths
    # ========================================================================
    op.create_table(
        'hadith_links',
        sa.Column('id', sa.Integer(), sa.Sequence('hadith_links_id_seq'), nullable=False),
        sa.Column('hadith_id', sa.Integer(), nullable=False),
        sa.Column('related_hadith_id', sa.Integer(), nullable=False),
        sa.Column('version', sa.String(20), server_default=sa.text("'v1.0'"), nullable=False),
        sa.Column('link_type', sa.String(50), nullable=False),
        sa.Column('link_subtype', sa.String(100), nullable=True),
        sa.Column('confidence', sa.Numeric(4, 3), nullable=True),
        sa.Column('reasoning', sa.Text(), nullable=True),
        sa.Column('theme_label', sa.String(255), nullable=True),
        sa.Column('pedagogical_sequence', sa.Integer(), nullable=True),
        sa.Column('is_bidirectional', sa.Boolean(), server_default=sa.text('FALSE'), nullable=True),
        sa.Column('detected_by', sa.String(50), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['hadith_id'], ['raw_hadiths.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['related_hadith_id'], ['raw_hadiths.id'], ondelete='CASCADE'),
        sa.CheckConstraint('hadith_id != related_hadith_id', name='check_different_hadiths'),
        sa.CheckConstraint(
            "link_type IN ('abrogation', 'tension', 'theme', 'pedagogical', 'corroboration')",
            name='check_link_type'
        )
    )

    # Indexes for hadith_links
    op.create_index('idx_links_hadith', 'hadith_links', ['hadith_id', 'version'])
    op.create_index('idx_links_related', 'hadith_links', ['related_hadith_id', 'version'])
    op.create_index('idx_links_type', 'hadith_links', ['link_type', 'version'])
    op.execute("""
        CREATE UNIQUE INDEX idx_unique_link ON hadith_links(
            LEAST(hadith_id, related_hadith_id),
            GREATEST(hadith_id, related_hadith_id),
            link_type,
            version
        ) WHERE is_bidirectional = TRUE
    """)

    # ========================================================================
    # TABLE 7: validation_results - Validation outcomes
    # ========================================================================
    op.create_table(
        'validation_results',
        sa.Column('id', sa.Integer(), sa.Sequence('validation_results_id_seq'), nullable=False),
        sa.Column('hadith_id', sa.Integer(), nullable=False),
        sa.Column('version', sa.String(20), server_default=sa.text("'v1.0'"), nullable=False),
        sa.Column('validation_type', sa.String(100), nullable=False),
        sa.Column('validation_category', sa.String(50), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('issues', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('quality_score', sa.Numeric(4, 3), nullable=True),
        sa.Column('temporal_confidence', sa.Numeric(4, 3), nullable=True),
        sa.Column('semantic_completeness', sa.Numeric(4, 3), nullable=True),
        sa.Column('validation_pass_rate', sa.Numeric(4, 3), nullable=True),
        sa.Column('validated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('validator_version', sa.String(20), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['hadith_id'], ['raw_hadiths.id'], ondelete='CASCADE'),
        sa.CheckConstraint("status IN ('pass', 'warning', 'fail')", name='check_status'),
        sa.CheckConstraint(
            "validation_category IN ('temporal', 'semantic', 'consistency', 'overall')",
            name='check_category'
        )
    )

    # Indexes for validation_results
    op.create_index('idx_validation_hadith_version', 'validation_results', ['hadith_id', 'version'])
    op.create_index('idx_validation_status', 'validation_results', ['status', 'version'])
    op.execute("CREATE INDEX idx_validation_issues ON validation_results USING gin(issues)")


def downgrade() -> None:
    """Drop all tables in reverse order."""
    op.drop_table('validation_results')
    op.drop_table('hadith_links')
    op.drop_table('hmsts_tags')
    op.drop_table('pcap_assignments')
    op.drop_table('temporal_markers')
    op.drop_table('preprocessed_hadiths')
    op.drop_table('raw_hadiths')
