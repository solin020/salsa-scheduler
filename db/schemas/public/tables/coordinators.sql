--
-- Name: coordinators; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.coordinators (
    projects text[],
    id text PRIMARY KEY
);


ALTER TABLE public.coordinators OWNER TO salsa_root;

--
-- Name: TABLE coordinators; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.coordinators TO admin;
GRANT SELECT ON TABLE public.coordinators TO coordinator;

--
-- Name: coordinators coordinator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY coordinator ON public.coordinators FOR SELECT TO coordinator USING ((id = current_setting('salsa.id'::text)));

--
-- Name: coordinators; Type: ROW SECURITY; Schema: public; Owner: postgres
--

ALTER TABLE public.coordinators ENABLE ROW LEVEL SECURITY;
