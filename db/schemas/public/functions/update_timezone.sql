--
-- Name: update_timezone(text, text); Type: PROCEDURE; Schema: public; Owner: salsa_root
--

CREATE PROCEDURE public.update_timezone(IN participant_id text, IN new_timezone text)
    LANGUAGE sql
    AS $$ 
  UPDATE message_schedule SET time=convert_timezone(time, P.old_timezone, new_timezone) FROM (SELECT timezone AS old_timezone FROM participants WHERE participants.id=participant_id) AS P WHERE participant_id=participant_id AND tries=0;
  UPDATE participants SET timezone=new_timezone WHERE id=participant_id;
$$;


ALTER PROCEDURE public.update_timezone(IN participant_id text, IN new_timezone text) OWNER TO salsa_root;
