--
-- Name: define_query(text); Type: FUNCTION; Schema: public; Owner: salsa_root
--

CREATE FUNCTION public.define_query(query text) RETURNS TABLE(column_name text, data_type text, is_nullable text)
    LANGUAGE plpgsql
    AS $_$ 
DECLARE 
v_view_n TEXT := 'temp_view$'; 
BEGIN 
       EXECUTE format( 'CREATE OR REPLACE TEMP VIEW  %I AS %s', v_view_n,query);
       RETURN QUERY  select i.column_name::text, i.data_type ::text, i.is_nullable::text
           from information_schema.columns i where i.table_name = v_view_n;
END $_$;


ALTER FUNCTION public.define_query(query text) OWNER TO salsa_root;
