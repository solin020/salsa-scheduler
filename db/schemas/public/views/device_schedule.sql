--
-- Name: device_schedule; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.device_schedule AS
 SELECT (to_char("time", 'YYYY'::text))::integer AS year,
    (to_char("time", 'MM'::text))::integer AS month,
    (to_char("time", 'DD'::text))::integer AS day,
    sequence_no,
    test_prototype_id
   FROM public.message_schedule
  WHERE (participant_id = current_setting('salsa.id'::text));


ALTER VIEW public.device_schedule OWNER TO salsa_root;

--
-- Name: TABLE device_schedule; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.device_schedule TO device;
