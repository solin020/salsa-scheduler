--
-- Name: participants; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.participants (
    projects text[],
    phone_number text,
    id text PRIMARY KEY,
    dropout boolean DEFAULT false,
    schedule_prototype_id text,
    schedule jsonb NOT NULL,
    twilio_nickname text,
    dashboard_code text DEFAULT 'not-assigned'::text,
    timezone text DEFAULT 'America/Chicago'::text NOT NULL
);


ALTER TABLE public.participants OWNER TO postgres;

--
-- Name: TABLE participants; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.participants TO admin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.participants TO coordinator;
GRANT SELECT ON TABLE public.participants TO device;


ALTER TABLE ONLY public.participants
    ADD CONSTRAINT participants_schedule_prototype_id_fkey FOREIGN KEY (schedule_prototype_id) REFERENCES public.schedule_prototype(id);

--
-- Name: participants coordinator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY coordinator ON public.participants TO coordinator USING ((EXISTS ( SELECT participants.id
   FROM public.coordinators
  WHERE ((coordinators.projects && participants.projects) AND (coordinators.id = current_setting('salsa.id'::text))))));

--
-- Name: participants device; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY device ON public.participants FOR SELECT TO device USING ((id = current_setting('salsa.id'::text)));

--
-- Name: participants; Type: ROW SECURITY; Schema: public; Owner: postgres
--

ALTER TABLE public.participants ENABLE ROW LEVEL SECURITY;
