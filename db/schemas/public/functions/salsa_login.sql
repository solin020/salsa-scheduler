--
-- Name: salsa_login(text); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.salsa_login(IN salsa_id text)
    LANGUAGE plpgsql
    AS $$
BEGIN
  RESET ROLE;
  EXECUTE FORMAT('SET salsa.id=%I', salsa_id);
  IF (EXISTS(SELECT id FROM admins WHERE id=salsa_id)) THEN
    SET ROLE admin;
  ELSIF (EXISTS(SELECT id FROM coordinators WHERE id=salsa_id)) THEN
    SET ROLE coordinator;
  ELSIF (EXISTS(SELECT id FROM annotators WHERE id=salsa_id)) THEN
    SET ROLE annotator;
  ELSE 
    SET ROLE device;
  END IF;
END;
$$;

ALTER PROCEDURE public.salsa_login(IN salsa_id text) OWNER TO postgres;
