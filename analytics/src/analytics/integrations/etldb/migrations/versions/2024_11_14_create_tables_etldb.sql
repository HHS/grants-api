CREATE TABLE IF NOT EXISTS gh_schema_version (
	version INTEGER NOT NULL UNIQUE,
	t_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	t_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO gh_schema_version (version) values (1) ON CONFLICT (version) DO NOTHING;

CREATE TABLE IF NOT EXISTS gh_deliverable (
	id SERIAL PRIMARY KEY,
	ghid TEXT UNIQUE NOT NULL,
	title TEXT NOT NULL,
	pillar TEXT, 
	t_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	t_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS gh_deliverable_quad_map (
	id SERIAL PRIMARY KEY,
	deliverable_id INTEGER NOT NULL,
	quad_id INTEGER,
	d_effective DATE NOT NULL,
	t_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	t_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	UNIQUE(deliverable_id, d_effective)
);
CREATE INDEX IF NOT EXISTS gh_dqm_i1 on gh_deliverable_quad_map(quad_id, d_effective);

CREATE TABLE IF NOT EXISTS gh_epic (
	id SERIAL PRIMARY KEY,
	ghid TEXT UNIQUE NOT NULL,
	title TEXT NOT NULL,
	t_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	t_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS gh_epic_deliverable_map (
	id SERIAL PRIMARY KEY,
	epic_id INTEGER NOT NULL,
	deliverable_id INTEGER,
	d_effective DATE NOT NULL,
	t_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	t_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	UNIQUE(epic_id, d_effective)
);
CREATE INDEX IF NOT EXISTS gh_edm_i1 on gh_epic_deliverable_map(deliverable_id, d_effective);

CREATE TABLE IF NOT EXISTS gh_issue (
	id SERIAL PRIMARY KEY,
	ghid TEXT UNIQUE NOT NULL,
	title TEXT NOT NULL,
	type TEXT NOT NULL,
	opened_date DATE,
	closed_date DATE,
	parent_issue_ghid TEXT,
	epic_id INTEGER,
	t_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	t_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS gh_issue_i1 on gh_issue(epic_id);

CREATE TABLE IF NOT EXISTS gh_issue_history (
	id SERIAL PRIMARY KEY,
	issue_id INTEGER NOT NULL,
	status TEXT,
	is_closed INTEGER NOT NULL,
	points INTEGER NOT NULL DEFAULT 0,
	d_effective DATE NOT NULL,
	t_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	t_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	UNIQUE(issue_id, d_effective)
);
CREATE INDEX IF NOT EXISTS gh_ih_i1 on gh_issue_history(issue_id, d_effective);

CREATE TABLE IF NOT EXISTS gh_issue_sprint_map (
	id SERIAL PRIMARY KEY,
	issue_id INTEGER NOT NULL,
	sprint_id INTEGER,
	d_effective DATE NOT NULL,
	t_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	t_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	UNIQUE(issue_id, d_effective)
);

CREATE TABLE IF NOT EXISTS gh_sprint (
	id SERIAL PRIMARY KEY,
	ghid TEXT UNIQUE NOT NULL,
	name TEXT NOT NULL,
	start_date DATE,
	end_date DATE,
	duration INTEGER,
	quad_id INTEGER,
	t_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	t_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS gh_quad (
	id SERIAL PRIMARY KEY,
	ghid TEXT UNIQUE NOT NULL,
	name TEXT NOT NULL,
	start_date DATE,
	end_date DATE,
	duration INTEGER,
	t_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	t_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS gh_quad_i1 on gh_quad(start_date);
 
