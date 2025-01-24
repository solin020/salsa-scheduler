--
-- Name: print_json(jsonb); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.print_json(j jsonb) RETURNS integer
    LANGUAGE plpython3u
    AS $$
import json; jj = json.loads(j);
return jj[1]

$$;


ALTER FUNCTION public.print_json(j jsonb) OWNER TO postgres;
