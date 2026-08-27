-- ============================================================
-- Career Intelligence Platform
-- MVP 1A - Synthetic Seed Data
--
-- Purpose:
-- Creates a deterministic synthetic dataset for development,
-- matching-model validation and Power BI prototyping.
--
-- IMPORTANT:
-- This script resets all current data in the MVP 1A tables.
-- ============================================================

BEGIN;


-- ============================================================
-- RESET
-- ============================================================

TRUNCATE TABLE
    fact_person_skill,
    bridge_job_skill,
    fact_job_posting,
    dim_person,
    dim_skill,
    dim_job_profile,
    dim_location,
    dim_company,
    dim_date,
    dim_proficiency
RESTART IDENTITY CASCADE;


-- ============================================================
-- DIM_PROFICIENCY
-- ============================================================

INSERT INTO dim_proficiency (
    proficiency_name,
    ordinal_rank
)
VALUES
    ('Beginner', 1),
    ('Intermediate', 2),
    ('Advanced', 3),
    ('Expert', 4);


-- ============================================================
-- DIM_DATE
-- ============================================================

INSERT INTO dim_date (
    date_key,
    full_date,
    year,
    quarter,
    month,
    month_name
)
VALUES
    (20260801, '2026-08-01', 2026, 3, 8, 'August'),
    (20260802, '2026-08-02', 2026, 3, 8, 'August'),
    (20260803, '2026-08-03', 2026, 3, 8, 'August'),
    (20260804, '2026-08-04', 2026, 3, 8, 'August'),
    (20260805, '2026-08-05', 2026, 3, 8, 'August'),
    (20260806, '2026-08-06', 2026, 3, 8, 'August'),
    (20260807, '2026-08-07', 2026, 3, 8, 'August'),
    (20260808, '2026-08-08', 2026, 3, 8, 'August'),
    (20260809, '2026-08-09', 2026, 3, 8, 'August'),
    (20260810, '2026-08-10', 2026, 3, 8, 'August');


-- ============================================================
-- DIM_SKILL
-- ============================================================

INSERT INTO dim_skill (
    skill_name,
    skill_category
)
VALUES
    ('R',                    'Technical Skill'),
    ('Shiny',                'Technical Skill'),
    ('Python',               'Technical Skill'),
    ('SQL',                  'Technical Skill'),
    ('Power BI',             'Technical Skill'),
    ('Java',                 'Technical Skill'),
    ('Docker',               'Technical Skill'),
    ('Statistics',           'Methodological Skill'),
    ('Machine Learning',     'Methodological Skill'),

    -- Skills deliberately absent from the synthetic person
    ('Azure',                'Technical Skill'),
    ('Kubernetes',           'Technical Skill'),
    ('Spark',                'Technical Skill'),
    ('SAS',                  'Technical Skill'),
    ('Spring Boot',          'Technical Skill');


-- ============================================================
-- DIM_COMPANY
-- ============================================================

INSERT INTO dim_company (
    company_name
)
VALUES
    ('Northstar Pharma'),
    ('Helix Clinical Research'),
    ('Hanseatic Analytics'),
    ('Nova Data Labs'),
    ('Quantive Health'),
    ('Scientific Systems GmbH'),
    ('CloudForge Technologies'),
    ('DataStream Engineering'),
    ('MachineWorks AI'),
    ('Enterprise Software Solutions');


-- ============================================================
-- DIM_LOCATION
-- ============================================================

INSERT INTO dim_location (
    city,
    region,
    country
)
VALUES
    ('Berlin',       'Berlin',               'Germany'),
    ('Hamburg',      'Hamburg',              'Germany'),
    ('Bremen',       'Bremen',               'Germany'),
    ('Munich',       'Bavaria',              'Germany'),
    ('Frankfurt',    'Hesse',                'Germany'),
    ('Hanover',      'Lower Saxony',         'Germany'),
    ('Oldenburg',    'Lower Saxony',         'Germany'),
    ('Cologne',      'North Rhine-Westphalia','Germany');


-- ============================================================
-- DIM_JOB_PROFILE
-- ============================================================

INSERT INTO dim_job_profile (
    profile_name
)
VALUES
    ('Statistical Programmer'),
    ('Biostatistician'),
    ('BI Analyst'),
    ('Data Scientist'),
    ('R/Shiny Developer'),
    ('Research Software Engineer'),
    ('Data Engineer'),
    ('Machine Learning Engineer'),
    ('Software Engineer');


-- ============================================================
-- DIM_PERSON
-- ============================================================

INSERT INTO dim_person (
    person_name
)
VALUES
    ('Synthetic Candidate');


-- ============================================================
-- FACT_PERSON_SKILL
--
-- Synthetic profile:
--
-- Strong:
--   R, Statistics
--
-- Good:
--   Python
--
-- Moderate:
--   SQL, Shiny, Java
--
-- Developing:
--   Power BI, Docker, Machine Learning
--
-- Missing:
--   Azure, Kubernetes, Spark, SAS, Spring Boot
-- ============================================================

INSERT INTO fact_person_skill (
    person_key,
    skill_key,
    proficiency_key,
    years_experience
)
SELECT
    p.person_key,
    s.skill_key,
    prof.proficiency_key,
    v.years_experience
FROM (
    VALUES
        ('R',                'Expert',       5.0::NUMERIC),
        ('Statistics',       'Expert',       6.0::NUMERIC),
        ('Python',           'Advanced',     3.0::NUMERIC),
        ('SQL',              'Intermediate', 2.0::NUMERIC),
        ('Shiny',            'Advanced',     2.5::NUMERIC),
        ('Power BI',         'Intermediate', 1.0::NUMERIC),
        ('Docker',           'Intermediate', 1.0::NUMERIC),
        ('Machine Learning', 'Intermediate', 1.5::NUMERIC),
        ('Java',             'Intermediate', 2.0::NUMERIC)
) AS v(skill_name, proficiency_name, years_experience)
JOIN dim_person p
    ON p.person_name = 'Synthetic Candidate'
JOIN dim_skill s
    ON s.skill_name = v.skill_name
JOIN dim_proficiency prof
    ON prof.proficiency_name = v.proficiency_name;


-- ============================================================
-- FACT_JOB_POSTING
--
-- The jobs are deliberately constructed to produce
-- different matching situations.
-- ============================================================

INSERT INTO fact_job_posting (
    source_job_id,
    job_title,
    date_key,
    company_key,
    location_key,
    job_profile_key,
    source_name
)
VALUES

    (
        'SYN-001',
        'Statistical Programmer',
        20260801,
        (SELECT company_key
         FROM dim_company
         WHERE company_name = 'Northstar Pharma'),
        (SELECT location_key
         FROM dim_location
         WHERE city = 'Berlin'),
        (SELECT job_profile_key
         FROM dim_job_profile
         WHERE profile_name = 'Statistical Programmer'),
        'Synthetic'
    ),

    (
        'SYN-002',
        'Biostatistician',
        20260802,
        (SELECT company_key
         FROM dim_company
         WHERE company_name = 'Helix Clinical Research'),
        (SELECT location_key
         FROM dim_location
         WHERE city = 'Hamburg'),
        (SELECT job_profile_key
         FROM dim_job_profile
         WHERE profile_name = 'Biostatistician'),
        'Synthetic'
    ),

    (
        'SYN-003',
        'Business Intelligence Analyst',
        20260803,
        (SELECT company_key
         FROM dim_company
         WHERE company_name = 'Hanseatic Analytics'),
        (SELECT location_key
         FROM dim_location
         WHERE city = 'Bremen'),
        (SELECT job_profile_key
         FROM dim_job_profile
         WHERE profile_name = 'BI Analyst'),
        'Synthetic'
    ),

    (
        'SYN-004',
        'Data Scientist',
        20260804,
        (SELECT company_key
         FROM dim_company
         WHERE company_name = 'Nova Data Labs'),
        (SELECT location_key
         FROM dim_location
         WHERE city = 'Munich'),
        (SELECT job_profile_key
         FROM dim_job_profile
         WHERE profile_name = 'Data Scientist'),
        'Synthetic'
    ),

    (
        'SYN-005',
        'R/Shiny Developer',
        20260805,
        (SELECT company_key
         FROM dim_company
         WHERE company_name = 'Quantive Health'),
        (SELECT location_key
         FROM dim_location
         WHERE city = 'Oldenburg'),
        (SELECT job_profile_key
         FROM dim_job_profile
         WHERE profile_name = 'R/Shiny Developer'),
        'Synthetic'
    ),

    (
        'SYN-006',
        'Research Software Engineer',
        20260806,
        (SELECT company_key
         FROM dim_company
         WHERE company_name = 'Scientific Systems GmbH'),
        (SELECT location_key
         FROM dim_location
         WHERE city = 'Hanover'),
        (SELECT job_profile_key
         FROM dim_job_profile
         WHERE profile_name = 'Research Software Engineer'),
        'Synthetic'
    ),

    (
        'SYN-007',
        'Senior Data Engineer',
        20260807,
        (SELECT company_key
         FROM dim_company
         WHERE company_name = 'DataStream Engineering'),
        (SELECT location_key
         FROM dim_location
         WHERE city = 'Frankfurt'),
        (SELECT job_profile_key
         FROM dim_job_profile
         WHERE profile_name = 'Data Engineer'),
        'Synthetic'
    ),

    (
        'SYN-008',
        'Cloud Data Engineer',
        20260808,
        (SELECT company_key
         FROM dim_company
         WHERE company_name = 'CloudForge Technologies'),
        (SELECT location_key
         FROM dim_location
         WHERE city = 'Cologne'),
        (SELECT job_profile_key
         FROM dim_job_profile
         WHERE profile_name = 'Data Engineer'),
        'Synthetic'
    ),

    (
        'SYN-009',
        'Machine Learning Engineer',
        20260809,
        (SELECT company_key
         FROM dim_company
         WHERE company_name = 'MachineWorks AI'),
        (SELECT location_key
         FROM dim_location
         WHERE city = 'Munich'),
        (SELECT job_profile_key
         FROM dim_job_profile
         WHERE profile_name = 'Machine Learning Engineer'),
        'Synthetic'
    ),

    (
        'SYN-010',
        'Senior Java Backend Developer',
        20260810,
        (SELECT company_key
         FROM dim_company
         WHERE company_name = 'Enterprise Software Solutions'),
        (SELECT location_key
         FROM dim_location
         WHERE city = 'Berlin'),
        (SELECT job_profile_key
         FROM dim_job_profile
         WHERE profile_name = 'Software Engineer'),
        'Synthetic'
    );


-- ============================================================
-- BRIDGE_JOB_SKILL
--
-- One row represents one skill requirement of one job.
--
-- Each synthetic job is intentionally designed to represent
-- a different matching scenario.
-- ============================================================

INSERT INTO bridge_job_skill (
    job_posting_key,
    skill_key,
    required_proficiency_key,
    required_years_experience
)
SELECT
    j.job_posting_key,
    s.skill_key,
    prof.proficiency_key,
    v.required_years_experience
FROM (
    VALUES

        -- ====================================================
        -- SYN-001
        -- Expected: Very strong match
        -- ====================================================
        ('SYN-001', 'R',          'Advanced',     3.0::NUMERIC),
        ('SYN-001', 'Statistics', 'Advanced',     3.0::NUMERIC),
        ('SYN-001', 'SQL',        'Intermediate', 1.0::NUMERIC),

        -- ====================================================
        -- SYN-002
        -- Expected: Strong match
        -- ====================================================
        ('SYN-002', 'R',          'Advanced',     3.0::NUMERIC),
        ('SYN-002', 'Statistics', 'Expert',       4.0::NUMERIC),
        ('SYN-002', 'Python',     'Intermediate', 1.0::NUMERIC),

        -- ====================================================
        -- SYN-003
        -- Expected: Moderate match
        -- Proficiency and experience deficits in Power BI/SQL
        -- ====================================================
        ('SYN-003', 'Power BI',   'Advanced',     2.0::NUMERIC),
        ('SYN-003', 'SQL',        'Advanced',     3.0::NUMERIC),
        ('SYN-003', 'Python',     'Intermediate', 1.0::NUMERIC),

        -- ====================================================
        -- SYN-004
        -- Expected: Good but imperfect match
        -- Machine Learning is deliberately demanding
        -- ====================================================
        ('SYN-004', 'Python',           'Advanced',     3.0::NUMERIC),
        ('SYN-004', 'Statistics',       'Advanced',     3.0::NUMERIC),
        ('SYN-004', 'Machine Learning', 'Advanced',     3.0::NUMERIC),
        ('SYN-004', 'SQL',              'Intermediate', 2.0::NUMERIC),

        -- ====================================================
        -- SYN-005
        -- Expected: Excellent match
        -- ====================================================
        ('SYN-005', 'R',          'Advanced', 3.0::NUMERIC),
        ('SYN-005', 'Shiny',      'Advanced', 2.0::NUMERIC),
        ('SYN-005', 'Statistics', 'Advanced', 2.0::NUMERIC),

        -- ====================================================
        -- SYN-006
        -- Expected: Mixed / reasonably good match
        -- ====================================================
        ('SYN-006', 'Python', 'Advanced',     3.0::NUMERIC),
        ('SYN-006', 'Java',   'Advanced',     3.0::NUMERIC),
        ('SYN-006', 'Docker', 'Intermediate', 1.0::NUMERIC),

        -- ====================================================
        -- SYN-007
        -- Expected: Weak match
        -- High requirements across familiar skills
        -- plus missing Spark
        -- ====================================================
        ('SYN-007', 'Python', 'Expert',   6.0::NUMERIC),
        ('SYN-007', 'SQL',    'Expert',   5.0::NUMERIC),
        ('SYN-007', 'Docker', 'Advanced', 3.0::NUMERIC),
        ('SYN-007', 'Spark',  'Advanced', 3.0::NUMERIC),

        -- ====================================================
        -- SYN-008
        -- Expected: Very weak match
        -- Azure and Kubernetes are completely missing
        -- ====================================================
        ('SYN-008', 'Python',     'Advanced', 4.0::NUMERIC),
        ('SYN-008', 'SQL',        'Advanced', 4.0::NUMERIC),
        ('SYN-008', 'Azure',      'Advanced', 3.0::NUMERIC),
        ('SYN-008', 'Kubernetes', 'Advanced', 3.0::NUMERIC),

        -- ====================================================
        -- SYN-009
        -- Expected: Weak-to-moderate match
        -- ====================================================
        ('SYN-009', 'Python',           'Expert',   4.0::NUMERIC),
        ('SYN-009', 'Machine Learning', 'Advanced', 3.0::NUMERIC),
        ('SYN-009', 'Docker',           'Advanced', 2.0::NUMERIC),

        -- ====================================================
        -- SYN-010
        -- Expected: Weak match
        -- Some Java experience exists, Spring Boot does not
        -- ====================================================
        ('SYN-010', 'Java',        'Advanced', 5.0::NUMERIC),
        ('SYN-010', 'Spring Boot', 'Advanced', 4.0::NUMERIC),
        ('SYN-010', 'Docker',      'Advanced', 3.0::NUMERIC),
        ('SYN-010', 'SQL',         'Advanced', 3.0::NUMERIC)

) AS v(
    source_job_id,
    skill_name,
    proficiency_name,
    required_years_experience
)
JOIN fact_job_posting j
    ON j.source_job_id = v.source_job_id
JOIN dim_skill s
    ON s.skill_name = v.skill_name
JOIN dim_proficiency prof
    ON prof.proficiency_name = v.proficiency_name;


COMMIT;