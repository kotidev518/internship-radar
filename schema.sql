-- RAW SCRAPED JOB DATA

CREATE TABLE raw_jobs (
id SERIAL PRIMARY KEY,
title TEXT,
company TEXT,
location TEXT,
description TEXT,
apply_link TEXT UNIQUE,
source TEXT,
processed BOOLEAN DEFAULT FALSE,
scraped_at TIMESTAMP DEFAULT NOW()
);

-- CLEAN INTERNSHIP RECORDS

CREATE TABLE internships (
id SERIAL PRIMARY KEY,
role TEXT,
company TEXT,
location TEXT,
skills TEXT[],
category TEXT,
remote BOOLEAN,
stipend TEXT,
apply_link TEXT UNIQUE,
source TEXT,
created_at TIMESTAMP DEFAULT NOW()
);

-- APPLICATION TRACKER

CREATE TABLE applications (
id SERIAL PRIMARY KEY,
internship_id INT REFERENCES internships(id) ON DELETE CASCADE,
status TEXT DEFAULT 'saved',
notes TEXT,
applied_date TIMESTAMP,
updated_at TIMESTAMP DEFAULT NOW()
);

-- INDEXES

CREATE INDEX idx_role
ON internships(role);

CREATE INDEX idx_category
ON internships(category);

CREATE INDEX idx_skills
ON internships USING GIN(skills);
