SELECT COUNT(*) AS job_count
FROM fact_job_posting;

SELECT COUNT(*) AS person_skill_count
FROM fact_person_skill;

SELECT
    j.source_job_id,
    j.job_title,
    s.skill_name,
    prof.proficiency_name AS required_proficiency,
    b.required_years_experience
FROM bridge_job_skill b
JOIN fact_job_posting j
    ON j.job_posting_key = b.job_posting_key
JOIN dim_skill s
    ON s.skill_key = b.skill_key
LEFT JOIN dim_proficiency prof
    ON prof.proficiency_key = b.required_proficiency_key
ORDER BY
    j.source_job_id,
    s.skill_name;


SELECT
    p.person_name,
    s.skill_name,
    prof.proficiency_name,
    prof.ordinal_rank,
    fps.years_experience
FROM fact_person_skill fps
JOIN dim_person p
    ON p.person_key = fps.person_key
JOIN dim_skill s
    ON s.skill_key = fps.skill_key
LEFT JOIN dim_proficiency prof
    ON prof.proficiency_key = fps.proficiency_key
ORDER BY
    s.skill_name;