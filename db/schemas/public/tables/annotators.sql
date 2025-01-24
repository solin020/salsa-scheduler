--
-- Name: annotators; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.annotators (
    projects text[],
    id text  PRIMARY KEY
);


ALTER TABLE public.annotators OWNER TO salsa_root;

--
-- Name: TABLE annotators; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.annotators TO admin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.annotators TO coordinator;
GRANT SELECT ON TABLE public.annotators TO annotator;


--
-- Name: annotators annotator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY annotator ON public.annotators FOR SELECT TO annotator USING ((id = current_setting('salsa.id'::text)));

--
-- Name: annotators; Type: ROW SECURITY; Schema: public; Owner: postgres
--

--
-- Name: annotators coordinator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY coordinator ON public.annotators TO coordinator USING ((EXISTS ( SELECT annotators.id
   FROM public.coordinators
  WHERE ((coordinators.projects && annotators.projects) AND (coordinators.id = current_setting('salsa.id'::text))))));


ALTER TABLE public.annotators ENABLE ROW LEVEL SECURITY;
