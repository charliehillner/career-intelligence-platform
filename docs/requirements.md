# 1. Vision

The vision of this project is to build a Business Intelligence platform that enables users to analyse labour market trends, understand their own professional profile, and make data-driven career decisions.

Rather than serving as a static reporting dashboard, the platform aims to provide actionable insights that help users identify opportunities for professional growth and improve their competitiveness in the job market.

# 2. Goal

The primary goal of this project is to demonstrate a complete Business Intelligence workflow.

The project covers

- data acquisition,
- ETL using Power Query,
- dimensional modelling using a star schema,
- analytical modelling with DAX,
- interactive dashboards in Power BI, and
- decision support based on labour market analytics.

The resulting platform should enable users to compare their own skills and experience with current market demand and derive concrete recommendations for future learning and career development.

# 3. Stakeholder

Individuals that might have a vested interested in this project are

- Job seekers
- Career changers
- Students and graduates
- Recruiters
- HR departments
- Business Intelligence analysts
- Labour market analysts

# 4. Business Questions

We divide business understanding into three levels:

## Level 1 - Understanding the job market

- What skills are sought after?
- What technologies are often asked for together?
- Which regions seek which profiles?
- What industries prefer which profiles?
- How does demand change over time?
- Which experience levels are expected?

## Level 2 - Understanding yourself

- What skills do I have?
- How much experience (in years) do I have?
- Which projects prove my skills?
- How do my skills develop over time?

## Level 3 – Decision Support

- Which skill gaps should be prioritised?
- Which additional skills would provide the greatest increase in marketability?
- Which regions best match my current profile?
- Which companies are realistic targets?
- Which technologies should I learn next?
- What salary range is realistic based on my profile?
- Which career paths appear to be the best fit?

# 5. Functional Requirements

The system shall

- analyse labour market trends
- analyse demand for individual skills
- compare regions
- compare industries
- analyse salary distributions
- identify skill gaps
- compare a personal profile with current market demand
- provide interactive filtering
- calculate analytical measures
- generate decision-support recommendations

# 6 Non-Functional Requirements

For example:

- The data model shall follow a star schema.
- Power BI shall be used as the reporting platform.
- Power Query shall be used for ETL processes.
- The solution shall support incremental extension by additional job platforms.
- The dimensional model shall remain extensible.
- The dashboard shall remain responsive and interactive.
- All transformations shall be reproducible.

# 7. Scope

Version 1 includes

- analysis of one job platform
- labour market analytics
- personal skill profile
- skill-gap analysis
- decision support
- Power BI dashboards

Future versions may include

- multiple job platforms
- automated data collection
- AI-assisted skill extraction
- forecasting
- personalised learning recommendations
