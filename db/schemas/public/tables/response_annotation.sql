--
-- Name: response_annotation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.response_annotation (
    schedule_id text,
    "timestamp" timestamp with time zone,
    annotation_file text,
    project text,
    annotator_id text
);


ALTER TABLE public.response_annotation OWNER TO postgres;

--
-- Name: TABLE response_annotation; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.response_annotation TO coordinator;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.response_annotation TO annotator;
GRANT ALL ON TABLE public.response_annotation TO admin;

--
-- Name: response_annotation coordinator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY coordinator ON public.response_annotation TO coordinator USING ((EXISTS ( SELECT coordinators.id
   FROM public.coordinators
  WHERE ((response_annotation.project = ANY (coordinators.projects)) AND (coordinators.id = current_setting('salsa.id'::text))))));

