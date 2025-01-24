--
-- Name: convert_timezone(timestamp with time zone, text, text); Type: FUNCTION; Schema: public; Owner: salsa_root
--


CREATE FUNCTION public.convert_timezone(timestamp with time zone, text, text) RETURNS timestamp with time zone
    LANGUAGE sql IMMUTABLE STRICT
    AS $_$SELECT (SELECT $1 at time zone $2 AS timestamp) at time zone $3 AS timestamptz;$_$;


ALTER FUNCTION public.convert_timezone(timestamp with time zone, text, text) OWNER TO salsa_root;