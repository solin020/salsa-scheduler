--
-- Name: transcription; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transcription (
    schedule_id text,
    stimulus_id text,
    score real,
    project text,
    segments jsonb
);


ALTER TABLE public.transcription OWNER TO postgres;

--
-- Name: TABLE transcription; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.transcription TO coordinator;
GRANT SELECT ON TABLE public.transcription TO annotator;
GRANT ALL ON TABLE public.transcription TO admin;
GRANT ALL ON TABLE public.transcription TO salsa;
GRANT INSERT ON TABLE public.transcription TO device;

--
-- Name: transcription annotators; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY annotators ON public.transcription TO annotator USING ((EXISTS ( SELECT annotators.id
   FROM public.annotators
  WHERE ((transcription.project = ANY (annotators.projects)) AND (annotators.id = current_setting('salsa.id'::text))))));


--
-- Name: transcription coordinators; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY coordinators ON public.transcription TO coordinator USING ((EXISTS ( SELECT coordinators.id
   FROM public.coordinators
  WHERE ((transcription.project = ANY (coordinators.projects)) AND (coordinators.id = current_setting('salsa.id'::text))))));


--
-- Name: transcription device; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY device ON public.transcription TO device USING (true);



--
-- Name: transcription; Type: ROW SECURITY; Schema: public; Owner: postgres
--

ALTER TABLE public.transcription ENABLE ROW LEVEL SECURITY;
