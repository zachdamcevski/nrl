-- create the competition table
CREATE TABLE competition (
  id INT PRIMARY KEY,
  name TEXT
);

-- insert data into competition table
INSERT INTO competition (id, name) VALUES (111, 'Telstra Premiership');

-- create team table
CREATE TABLE team (
  id INT PRIMARY KEY,
  name TEXT,
  nickname TEXT
) ;

-- insert into team

INSERT INTO team (id, name, nickname) VALUES (500031, 'Parramatta Eels', 'Eels');
INSERT INTO team (id, name, nickname) VALUES (500021, 'Melbourne Storm', 'Storm');
INSERT INTO team (id, name, nickname) VALUES (500032, 'Warriors', 'Warriors');
INSERT INTO team (id, name, nickname) VALUES (500003, 'Newcastle Knights', 'Knights');
INSERT INTO team (id, name, nickname) VALUES (500014, 'Penrith Panthers', 'Panthers');
INSERT INTO team (id, name, nickname) VALUES (500011, 'Brisbane Broncos', 'Broncos');
INSERT INTO team (id, name, nickname) VALUES (500002, 'Manly-Warringah Sea Eagles', 'Sea Eagles');
INSERT INTO team (id, name, nickname) VALUES (500010, 'Canterbury-Bankstown Bulldogs', 'Bulldogs');
INSERT INTO team (id, name, nickname) VALUES (500012, 'North Queensland Cowboys', 'Cowboys');
INSERT INTO team (id, name, nickname) VALUES (500013, 'Canberra Raiders', 'Raiders');
INSERT INTO team (id, name, nickname) VALUES (500028, 'Cronulla-Sutherland Sharks', 'Sharks');
INSERT INTO team (id, name, nickname) VALUES (500005, 'South Sydney Rabbitohs', 'Rabbitohs');
INSERT INTO team (id, name, nickname) VALUES (500723, 'Dolphins', 'Dolphins');
INSERT INTO team (id, name, nickname) VALUES (500001, 'Sydney Roosters', 'Roosters');
INSERT INTO team (id, name, nickname) VALUES (500023, 'Wests Tigers', 'Wests Tigers');
INSERT INTO team (id, name, nickname) VALUES (500004, 'Gold Coast Titans', 'Titans');
INSERT INTO team (id, name, nickname) VALUES (500022, 'St. George Illawarra Dragons', 'Dragons');

-- create the match table
CREATE TABLE game (
  id BIGINT PRIMARY KEY,
  round_number INT,
  competition_id INT,
  home_team_id INT,
  away_team_id INT,
  start_time TEXT,
  stadium TEXT,
  city TEXT,
  attendence INT,
  ground_conditions TEXT,
  home_team_score INT,
  away_team_score INT,
  FOREIGN KEY(competition_id) REFERENCES competition(id),
  FOREIGN KEY(home_team_id) REFERENCES team(id),
  FOREIGN KEY(away_team_id) REFERENCES team(id)
);

-- create the playerGameStatistics table
CREATE TABLE playerGameStatistics (
  id VARCHAR(128),
  player_id INT,
  player_team_id INT,
  player_name VARCHAR(128),
  player_position VARCHAR(128),
  game_id BIGINT,
  all_run_metres INT,
  all_runs INT,
  bomb_kicks INT,
  cross_field_kicks INT,
  conversions INT,
  conversion_attempts INT,
  dummy_half_runs INT,
  dummy_half_run_metres INT,
  dummy_passes INT,
  errors INT,
  fantasy_points_total INT,
  field_goals INT,
  forced_drop_out_kicks INT,
  forty_twenty_kicks INT,
  goals INT,
  goal_conversion_rate FLOAT,
  grubber_kicks INT,
  handling_errors INT,
  hit_ups INT,
  hit_up_run_metres INT,
  ineffective_tackles INT,
  intercepts INT,
  kicks INT,
  kicks_dead INT,
  kicks_defused INT,
  kick_metres INT,
  kick_return_metres INT,
  line_break_assists INT,
  line_breaks INT,
  line_engaged_runs INT,
  minutes_played INT,
  missed_tackles INT,
  offloads INT,
  offside_within_ten_metres INT,
  one_on_one_lost INT,
  one_on_one_steal INT,
  on_report BOOLEAN,
  passes_to_run_ratio FLOAT,
  passes INT,
  play_the_ball_total INT,
  play_the_ball_average_speed FLOAT,
  penalties INT,
  points INT,
  penalty_goals INT,
  post_contact_metres INT,
  receipts INT,
  ruck_infringements INT,
  send_offs INT,
  sin_bins INT,
  stint_one INT,
  tackle_breaks INT,
  tackle_efficiency FLOAT,
  tackles_made INT,
  tries INT,
  try_assists INT,
  twenty_forty_kicks INT,
  two_point_field_goals INT
);
