--
-- Name: all_projects; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.all_projects AS
 SELECT DISTINCT unnest(projects) AS projects
   FROM public.coordinators;


ALTER VIEW public.all_projects OWNER TO salsa_root;
