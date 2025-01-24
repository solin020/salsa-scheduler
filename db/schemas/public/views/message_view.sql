--
-- Name: message_view; Type: VIEW; Schema: public; Owner: salsa_root
--

CREATE VIEW public.message_view WITH (security_invoker='true') AS
 SELECT p.id AS participant_id,
    ((m."time" + m.bug_interval))::timestamp without time zone AS utc_time,
    ((m."time" + m.bug_interval) AT TIME ZONE p.timezone) AS their_time,
    m.message,
    m.condition,
    (m.tries > 0) AS sent
   FROM public.message_schedule m,
    public.participants p
  WHERE (p.id = m.participant_id);


ALTER VIEW public.message_view OWNER TO salsa_root;


--
-- Name: TABLE message_view; Type: ACL; Schema: public; Owner: salsa_root
--

GRANT SELECT ON TABLE public.message_view TO coordinator;
GRANT SELECT ON TABLE public.message_view TO admin;
