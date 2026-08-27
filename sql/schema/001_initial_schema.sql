-- ============================================================
-- Career Intelligence Platform
-- MVP 1A - Initial Analytical Schema
-- ============================================================


-- ============================================================
-- DIMENSIONS
-- ============================================================

CREATE TABLE dim_date (
    date_key        INTEGER PRIMARY KEY,
    full_date       DATE NOT NULL UNIQUE,
    year            SMALLINT NOT NULL,
    quarter         SMALLINT NOT NULL,
    month           SMALLINT NOT NULL,
    month_name      VARCHAR(20) NOT NULL
);


CREATE TABLE dim_company (
    company_key     BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    company_name    VARCHAR(255) NOT NULL UNIQUE
);


CREATE TABLE dim_location (
    location_key    BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    city            VARCHAR(150),
    region          VARCHAR(150),
    country         VARCHAR(150) NOT NULL
);


CREATE TABLE dim_job_profile (
    job_profile_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    profile_name    VARCHAR(150) NOT NULL UNIQUE
);


CREATE TABLE dim_skill (
    skill_key       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    skill_name      VARCHAR(150) NOT NULL UNIQUE,
    skill_category  VARCHAR(100)
);


CREATE TABLE dim_person (
    person_key      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    person_name     VARCHAR(150) NOT NULL
);

CREATE TABLE dim_proficiency (
    proficiency_key    SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    proficiency_name   VARCHAR(50) NOT NULL UNIQUE,
    ordinal_rank       SMALLINT NOT NULL UNIQUE,

    CONSTRAINT chk_proficiency_rank
        CHECK (ordinal_rank > 0)
);

-- ============================================================
-- FACT: JOB POSTING
-- Grain:
-- One row represents one observed job posting.
-- ============================================================

CREATE TABLE fact_job_posting (
    job_posting_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    source_job_id   VARCHAR(255),
    job_title       VARCHAR(255) NOT NULL,

    date_key        INTEGER NOT NULL,
    company_key     BIGINT,
    location_key    BIGINT,
    job_profile_key BIGINT,

    source_name     VARCHAR(100),

    CONSTRAINT fk_job_date
        FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key),

    CONSTRAINT fk_job_company
        FOREIGN KEY (company_key)
        REFERENCES dim_company(company_key),

    CONSTRAINT fk_job_location
        FOREIGN KEY (location_key)
        REFERENCES dim_location(location_key),

    CONSTRAINT fk_job_profile
        FOREIGN KEY (job_profile_key)
        REFERENCES dim_job_profile(job_profile_key)
);


-- ============================================================
-- BRIDGE: JOB <-> SKILL
-- Grain:
-- One row represents one skill requirement of one job posting.
-- ============================================================

CREATE TABLE bridge_job_skill (
    job_posting_key           BIGINT NOT NULL,
    skill_key                 BIGINT NOT NULL,
    required_proficiency_key  SMALLINT,
    required_years_experience NUMERIC(4,1),

    PRIMARY KEY (job_posting_key, skill_key),

    CONSTRAINT fk_job_skill_job
        FOREIGN KEY (job_posting_key)
        REFERENCES fact_job_posting(job_posting_key)
        ON DELETE CASCADE,

    CONSTRAINT fk_job_skill_skill
        FOREIGN KEY (skill_key)
        REFERENCES dim_skill(skill_key),

    CONSTRAINT fk_job_skill_proficiency
        FOREIGN KEY (required_proficiency_key)
        REFERENCES dim_proficiency(proficiency_key),

    CONSTRAINT chk_required_experience
        CHECK (
            required_years_experience IS NULL
            OR required_years_experience >= 0
        )
);


-- ============================================================
-- FACT: PERSON <-> SKILL
-- Grain:
-- One row represents one observed skill of one person.
-- ============================================================

CREATE TABLE fact_person_skill (
    person_key        BIGINT NOT NULL,
    skill_key         BIGINT NOT NULL,
    proficiency_key   SMALLINT,
    years_experience  NUMERIC(4,1),

    PRIMARY KEY (person_key, skill_key),

    CONSTRAINT fk_person_skill_person
        FOREIGN KEY (person_key)
        REFERENCES dim_person(person_key)
        ON DELETE CASCADE,

    CONSTRAINT fk_person_skill_skill
        FOREIGN KEY (skill_key)
        REFERENCES dim_skill(skill_key),

    CONSTRAINT fk_person_skill_proficiency
        FOREIGN KEY (proficiency_key)
        REFERENCES dim_proficiency(proficiency_key),

    CONSTRAINT chk_person_experience
        CHECK (
            years_experience IS NULL
            OR years_experience >= 0
        )
);