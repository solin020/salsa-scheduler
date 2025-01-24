--
-- Name: schedule_prototype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.schedule_prototype (
    project text NOT NULL,
    id text PRIMARY KEY,
    schedule jsonb NOT NULL
);


ALTER TABLE public.schedule_prototype OWNER TO salsa_root;

--
-- Name: TABLE schedule_prototype; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.schedule_prototype TO coordinator;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.schedule_prototype TO admin;

--
-- Name: schedule_prototype coordinator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY coordinator ON public.schedule_prototype TO coordinator USING ((EXISTS ( SELECT c.id
   FROM public.coordinators c
  WHERE ((c.id = current_setting('salsa.id'::text)) AND (schedule_prototype.project = ANY (c.projects))))));


--
-- Name: schedule_prototype; Type: ROW SECURITY; Schema: public; Owner: postgres
--

ALTER TABLE public.schedule_prototype ENABLE ROW LEVEL SECURITY;
