--
-- Name: generate_message_schedule_tfn(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.generate_message_schedule_tfn() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    PERFORM  generate_message_schedule(NEW.id); RETURN NEW;
END;
$$;


ALTER FUNCTION public.generate_message_schedule_tfn() OWNER TO postgres;