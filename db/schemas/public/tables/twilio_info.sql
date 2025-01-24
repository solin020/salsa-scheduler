--
-- Name: twilio_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.twilio_info (
    project text NOT NULL,
    account_sid text NOT NULL,
    auth_token text NOT NULL,
    phone_number text NOT NULL,
    nickname text PRIMARY KEY
);


ALTER TABLE public.twilio_info OWNER TO salsa_root;


--
-- Name: TABLE twilio_info; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.twilio_info TO coordinator;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.twilio_info TO admin;

--
-- Name: twilio_info coordinator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY coordinator ON public.twilio_info TO coordinator USING ((EXISTS ( SELECT c.id
   FROM public.coordinators c
  WHERE (twilio_info.project = ANY (c.projects)))));


--
-- Name: twilio_info; Type: ROW SECURITY; Schema: public; Owner: postgres
--

ALTER TABLE public.twilio_info ENABLE ROW LEVEL SECURITY;
