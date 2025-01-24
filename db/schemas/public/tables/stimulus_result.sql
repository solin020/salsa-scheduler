-- Name: stimulus_result; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stimulus_result (
    project text,
    participant_id text,
    real_timestamp timestamp with time zone,
    miscellaneous json,
    test_prototype_id text,
    schedule_id text DEFAULT 'future'::text NOT NULL,
    stimulus_id text,
    sequence_no integer,
    formal_timestamp timestamp with time zone,
    schedule_prototype_id text,
    quality text DEFAULT '0'::text,
    inspected boolean DEFAULT false
);


ALTER TABLE public.stimulus_result OWNER TO postgres;

--
-- Name: TABLE stimulus_result; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,UPDATE ON TABLE public.stimulus_result TO device;
GRANT ALL ON TABLE public.stimulus_result TO admin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.stimulus_result TO coordinator;
GRANT SELECT ON TABLE public.stimulus_result TO annotator;

--
-- Name: stimulus_result stimulus_result_schedule_prototype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stimulus_result
    ADD CONSTRAINT stimulus_result_schedule_prototype_id_fkey FOREIGN KEY (schedule_prototype_id) REFERENCES public.schedule_prototype(id);

--
-- Name: stimulus_result annotator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY annotator ON public.stimulus_result FOR SELECT TO annotator USING ((EXISTS ( SELECT annotators.id
   FROM public.annotators
  WHERE ((stimulus_result.project = ANY (annotators.projects)) AND (annotators.id = current_setting('salsa.id'::text))))));

--
-- Name: stimulus_result coordinator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY coordinator ON public.stimulus_result TO coordinator USING ((EXISTS ( SELECT coordinators.id
   FROM public.coordinators
  WHERE ((stimulus_result.project = ANY (coordinators.projects)) AND (coordinators.id = current_setting('salsa.id'::text))))));


--
-- Name: stimulus_result device; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY device ON public.stimulus_result TO device USING (true);

--
-- Name: stimulus_result; Type: ROW SECURITY; Schema: public; Owner: postgres
--

ALTER TABLE public.stimulus_result ENABLE ROW LEVEL SECURITY;
