CREATE TABLE links
(
    id VARCHAR(10) PRIMARY KEY NOT NULL,
    url VARCHAR,
    created TIMESTAMP
);
CREATE UNIQUE INDEX links_url_key ON links (url);

CREATE OR REPLACE FUNCTION sp_add_link (id character varying, url character varying) RETURNS TABLE(id character varying, url character varying)
	LANGUAGE sql
AS $$

with s as (
    select id, url
    from links
    where url = $2
), i as (
    insert into links (id, url)
    select $1, $2
    where not exists (select 1 from s)
    returning (select id from links l where l.url = $2), url
)
select id, url
from i
union all
select id, url
from s;
$$
