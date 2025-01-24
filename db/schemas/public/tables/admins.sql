--
-- Name: admins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admins (
    id text PRIMARY KEY
);


ALTER TABLE public.admins OWNER TO postgres;
--
-- Name: TABLE admins; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.admins TO admin;

