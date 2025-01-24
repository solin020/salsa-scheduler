--
-- Name: download_result; Type: VIEW; Schema: public; Owner: salsa_root
--

-- This prevents unsubmitted sitmulus results from appearing in the downloads and glitching them

CREATE VIEW public.download_result AS
 SELECT s.project,
    s.participant_id,
    s.real_timestamp,
    s.miscellaneous,
    s.test_prototype_id,
    s.schedule_id,
    s.stimulus_id,
    s.sequence_no,
    s.formal_timestamp,
    s.schedule_prototype_id,
        CASE
            WHEN ((s.quality = '0'::text) AND (s.formal_timestamp < now())) THEN '1'::text
            WHEN ((s.quality = '0'::text) AND p.dropout) THEN '100'::text
            WHEN ((s.quality = '0'::text) AND (s.formal_timestamp > now()) AND (s.formal_timestamp < (now() + '2 days'::interval))) THEN '99'::text
            WHEN ((s.quality = '0'::text) AND (s.formal_timestamp < now()) AND (s.formal_timestamp > (now() - '2 days'::interval))) THEN '98'::text
            ELSE s.quality
        END AS quality
   FROM public.stimulus_result s,
    public.participants p
  WHERE ((s.participant_id = p.id) AND (s.schedule_id <> 'future'::text));


ALTER VIEW public.download_result OWNER TO salsa_root;

--
-- Name: TABLE visit_result; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.download_result TO coordinator;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.download_result TO admin;

