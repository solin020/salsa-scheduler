--
-- Name: test_prototype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.test_prototype (
    project text,
    id text PRIMARY KEY,
    groups text[] DEFAULT '{}'::text[],
    randomized boolean DEFAULT false
);


ALTER TABLE public.test_prototype OWNER TO postgres;

--
-- Name: TABLE test_prototype; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.test_prototype TO admin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.test_prototype TO coordinator;
GRANT SELECT ON TABLE public.test_prototype TO device;
GRANT SELECT ON TABLE public.test_prototype TO annotator;

--
-- Name: test_prototype annotator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY annotator ON public.test_prototype FOR SELECT TO annotator USING ((EXISTS ( SELECT annotators.id
   FROM public.annotators
  WHERE ((test_prototype.project = ANY (annotators.projects)) AND (annotators.id = current_setting('salsa.id'::text))))));


--
-- Name: test_prototype coordinator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY coordinator ON public.test_prototype TO coordinator USING ((EXISTS ( SELECT coordinators.id
   FROM public.coordinators
  WHERE ((test_prototype.project = ANY (coordinators.projects)) AND (coordinators.id = current_setting('salsa.id'::text))))));

--
-- Name: test_prototype device; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY device ON public.test_prototype FOR SELECT TO device USING ((EXISTS ( SELECT participants.id
   FROM public.participants
  WHERE ((test_prototype.project = ANY (participants.projects)) AND (participants.id = current_setting('salsa.id'::text))))));

--
-- Name: test_prototype; Type: ROW SECURITY; Schema: public; Owner: postgres
--

ALTER TABLE public.test_prototype ENABLE ROW LEVEL SECURITY;
