--
-- Name: completionstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.completionstatus AS ENUM (
    '0',
    '1',
    '2',
    '3',
    '100'
);


ALTER TYPE public.completionstatus OWNER TO postgres;
