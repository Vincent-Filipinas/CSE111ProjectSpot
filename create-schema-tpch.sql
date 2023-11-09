CREATE TABLE artist (
    a_name       char(100) not null,
    a_artistkey decimal(3,0) not null
);


CREATE TABLE song (
    s_trackname       char(100) not null,
    s_artistkey  decimal(3,0) not null,
    s_artistcount  decimal(3,0) not null,
    s_released_year  decimal(4,0) not null,
    s_released_month  decimal(2,0) not null,
    s_released_day decimal(2,0) not null,
    s_streams decimal(14,0) not null,
    s_bpm decimal (3,0) not null,
    s_key char(2) not null,
    s_mode char(5) not null,
    s_songkey decimal(3,0) not null
);

CREATE TABLE playlist (
    p_inspotify_playlist decimal(6,0) not null,
    p_inapple_playlist decimal(6,0) not null,
    p_indeezer_playlist decimal(6,0) not null,
    p_songkey_playlist decimal(4,0) not null
);

CREATE TABLE stats (
    danceability_per decimal(2,0) not null,
    valence_per decimal (2,0) not null,
    energy_per decimal (2,0) not null,
    acousticness_per decimal (2,0) not null,
    instrumental_per decimal (2,0) not null,
    liveness_per decimal (2,0) not null,
    speechiness_per decimal (2,0) not null,
    st_songkey decimal (3,0) not null
);

CREATE TABLE charts (
    c_inspotify_chart decimal (4,0) not null,
    c_inapple_chart decimal (4,0) not null,
    c_indeezer_chart decimal (4,0) not null,
    c_inshazam_chrt decimal (4,0) not null,
    c_songkey decimal (4,0) not null
);