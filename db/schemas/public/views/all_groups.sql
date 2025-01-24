--
-- Name: all_groups; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.all_groups WITH (security_invoker='true') AS
 SELECT DISTINCT project,
    unnest(groups) AS "group"
   FROM public.test_prototype;


ALTER VIEW public.all_groups OWNER TO salsa_root;

--
-- Name: TABLE all_groups; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.all_groups TO coordinator;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.all_groups TO admin;
