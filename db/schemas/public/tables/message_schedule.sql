--
-- Name: message_schedule; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.message_schedule (
    tries integer DEFAULT 0,
    "time" timestamp with time zone,
    dest_number text,
    message text,
    max_tries integer DEFAULT 1,
    bug_interval interval DEFAULT '00:10:00'::interval,
    project text,
    test_prototype_id text,
    participant_id text,
    sequence_no integer DEFAULT '-1'::integer,
    twilio_info text,
    condition text
);


ALTER TABLE public.message_schedule OWNER TO salsa_root;

--
-- Name: TABLE message_schedule; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.message_schedule TO admin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.message_schedule TO coordinator;

ALTER TABLE ONLY public.message_schedule
    ADD CONSTRAINT fk_participant_id FOREIGN KEY (participant_id) REFERENCES public.participants(id) ON DELETE CASCADE;


--
-- Name: message_schedule coordinator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY coordinator ON public.message_schedule TO coordinator USING ((EXISTS ( SELECT coordinators.id
   FROM public.coordinators
  WHERE ((message_schedule.project = ANY (coordinators.projects)) AND (coordinators.id = current_setting('salsa.id'::text))))));

--
-- Name: message_schedule; Type: ROW SECURITY; Schema: public; Owner: postgres
--

ALTER TABLE public.message_schedule ENABLE ROW LEVEL SECURITY;
