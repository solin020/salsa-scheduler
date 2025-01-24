--
-- Name: delete_test_participants(); Type: PROCEDURE; Schema: public; Owner: salsa_root
--

CREATE PROCEDURE public.delete_test_participants()
    LANGUAGE plpgsql
    AS $$
BEGIN
  DELETE FROM participants WHERE id LIKE '%test%';
  DELETE FROM message_schedule WHERE participant_id LIKE '%test%';
  DELETE FROM stimulus_result WHERE participant_id LIKE '%test%';
END
$$;


ALTER PROCEDURE public.delete_test_participants() OWNER TO salsa_root;