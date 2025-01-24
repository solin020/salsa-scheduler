--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2 (Debian 16.2-1.pgdg120+2)
-- Dumped by pg_dump version 16.2 (Debian 16.2-1.pgdg120+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

--
-- Name: admins admins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY (id);


--
-- Name: annotators annotators_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annotators
    ADD CONSTRAINT annotators_pkey PRIMARY KEY (id);


--
-- Name: coordinators coordinators_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.coordinators
    ADD CONSTRAINT coordinators_pkey PRIMARY KEY (id);


--
-- Name: participants participants_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participants
    ADD CONSTRAINT participants_pkey PRIMARY KEY (id);


--
-- Name: schedule_prototype schedule_prototype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schedule_prototype
    ADD CONSTRAINT schedule_prototype_pkey PRIMARY KEY (id);


--
-- Name: stimulus stimulus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stimulus
    ADD CONSTRAINT stimulus_pkey PRIMARY KEY (id);


--
-- Name: test_prototype testprototype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.test_prototype
    ADD CONSTRAINT testprototype_pkey PRIMARY KEY (id);


--
-- Name: twilio_info twilio_info_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.twilio_info
    ADD CONSTRAINT twilio_info_pkey PRIMARY KEY (nickname);


--
-- Name: participants generate_message_schedule; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER generate_message_schedule AFTER INSERT ON public.participants FOR EACH ROW EXECUTE FUNCTION public.generate_message_schedule_tfn();


--
-- Name: message_schedule fk_participant_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message_schedule
    ADD CONSTRAINT fk_participant_id FOREIGN KEY (participant_id) REFERENCES public.participants(id) ON DELETE CASCADE;


--
-- Name: participants participants_schedule_prototype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participants
    ADD CONSTRAINT participants_schedule_prototype_id_fkey FOREIGN KEY (schedule_prototype_id) REFERENCES public.schedule_prototype(id);


--
-- Name: stimulus_result stimulus_result_schedule_prototype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stimulus_result
    ADD CONSTRAINT stimulus_result_schedule_prototype_id_fkey FOREIGN KEY (schedule_prototype_id) REFERENCES public.schedule_prototype(id);


--
-- Name: annotators annotator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY annotator ON public.annotators FOR SELECT TO annotator USING ((id = current_setting('salsa.id'::text)));


--
-- Name: response_annotation annotator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY annotator ON public.response_annotation TO annotator USING ((EXISTS ( SELECT annotators.id
   FROM public.annotators
  WHERE ((response_annotation.project = ANY (annotators.projects)) AND (annotators.id = current_setting('salsa.id'::text))))));


--
-- Name: stimulus_result annotator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY annotator ON public.stimulus_result FOR SELECT TO annotator USING ((EXISTS ( SELECT annotators.id
   FROM public.annotators
  WHERE ((stimulus_result.project = ANY (annotators.projects)) AND (annotators.id = current_setting('salsa.id'::text))))));


--
-- Name: test_prototype annotator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY annotator ON public.test_prototype FOR SELECT TO annotator USING ((EXISTS ( SELECT annotators.id
   FROM public.annotators
  WHERE ((test_prototype.project = ANY (annotators.projects)) AND (annotators.id = current_setting('salsa.id'::text))))));


--
-- Name: annotators; Type: ROW SECURITY; Schema: public; Owner: postgres
--

ALTER TABLE public.annotators ENABLE ROW LEVEL SECURITY;

--
-- Name: transcription annotators; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY annotators ON public.transcription TO annotator USING ((EXISTS ( SELECT annotators.id
   FROM public.annotators
  WHERE ((transcription.project = ANY (annotators.projects)) AND (annotators.id = current_setting('salsa.id'::text))))));


--
-- Name: annotators coordinator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY coordinator ON public.annotators TO coordinator USING ((EXISTS ( SELECT annotators.id
   FROM public.coordinators
  WHERE ((coordinators.projects && annotators.projects) AND (coordinators.id = current_setting('salsa.id'::text))))));


--
-- Name: coordinators coordinator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY coordinator ON public.coordinators FOR SELECT TO coordinator USING ((id = current_setting('salsa.id'::text)));


--
-- Name: message_schedule coordinator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY coordinator ON public.message_schedule TO coordinator USING ((EXISTS ( SELECT coordinators.id
   FROM public.coordinators
  WHERE ((message_schedule.project = ANY (coordinators.projects)) AND (coordinators.id = current_setting('salsa.id'::text))))));


--
-- Name: participants coordinator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY coordinator ON public.participants TO coordinator USING ((EXISTS ( SELECT participants.id
   FROM public.coordinators
  WHERE ((coordinators.projects && participants.projects) AND (coordinators.id = current_setting('salsa.id'::text))))));


--
-- Name: response_annotation coordinator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY coordinator ON public.response_annotation TO coordinator USING ((EXISTS ( SELECT coordinators.id
   FROM public.coordinators
  WHERE ((response_annotation.project = ANY (coordinators.projects)) AND (coordinators.id = current_setting('salsa.id'::text))))));


--
-- Name: schedule_prototype coordinator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY coordinator ON public.schedule_prototype TO coordinator USING ((EXISTS ( SELECT c.id
   FROM public.coordinators c
  WHERE ((c.id = current_setting('salsa.id'::text)) AND (schedule_prototype.project = ANY (c.projects))))));


--
-- Name: stimulus_result coordinator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY coordinator ON public.stimulus_result TO coordinator USING ((EXISTS ( SELECT coordinators.id
   FROM public.coordinators
  WHERE ((stimulus_result.project = ANY (coordinators.projects)) AND (coordinators.id = current_setting('salsa.id'::text))))));


--
-- Name: test_prototype coordinator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY coordinator ON public.test_prototype TO coordinator USING ((EXISTS ( SELECT coordinators.id
   FROM public.coordinators
  WHERE ((test_prototype.project = ANY (coordinators.projects)) AND (coordinators.id = current_setting('salsa.id'::text))))));


--
-- Name: twilio_info coordinator; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY coordinator ON public.twilio_info TO coordinator USING ((EXISTS ( SELECT c.id
   FROM public.coordinators c
  WHERE (twilio_info.project = ANY (c.projects)))));


--
-- Name: coordinators; Type: ROW SECURITY; Schema: public; Owner: postgres
--

ALTER TABLE public.coordinators ENABLE ROW LEVEL SECURITY;

--
-- Name: transcription coordinators; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY coordinators ON public.transcription TO coordinator USING ((EXISTS ( SELECT coordinators.id
   FROM public.coordinators
  WHERE ((transcription.project = ANY (coordinators.projects)) AND (coordinators.id = current_setting('salsa.id'::text))))));


--
-- Name: participants device; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY device ON public.participants FOR SELECT TO device USING ((id = current_setting('salsa.id'::text)));


--
-- Name: stimulus_result device; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY device ON public.stimulus_result TO device USING (true);


--
-- Name: test_prototype device; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY device ON public.test_prototype FOR SELECT TO device USING ((EXISTS ( SELECT participants.id
   FROM public.participants
  WHERE ((test_prototype.project = ANY (participants.projects)) AND (participants.id = current_setting('salsa.id'::text))))));


--
-- Name: transcription device; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY device ON public.transcription TO device USING (true);


--
-- Name: message_schedule; Type: ROW SECURITY; Schema: public; Owner: postgres
--

ALTER TABLE public.message_schedule ENABLE ROW LEVEL SECURITY;

--
-- Name: participants; Type: ROW SECURITY; Schema: public; Owner: postgres
--

ALTER TABLE public.participants ENABLE ROW LEVEL SECURITY;

--
-- Name: schedule_prototype; Type: ROW SECURITY; Schema: public; Owner: postgres
--

ALTER TABLE public.schedule_prototype ENABLE ROW LEVEL SECURITY;

--
-- Name: stimulus_result; Type: ROW SECURITY; Schema: public; Owner: postgres
--

ALTER TABLE public.stimulus_result ENABLE ROW LEVEL SECURITY;

--
-- Name: test_prototype; Type: ROW SECURITY; Schema: public; Owner: postgres
--

ALTER TABLE public.test_prototype ENABLE ROW LEVEL SECURITY;

--
-- Name: transcription; Type: ROW SECURITY; Schema: public; Owner: postgres
--

ALTER TABLE public.transcription ENABLE ROW LEVEL SECURITY;

--
-- Name: twilio_info; Type: ROW SECURITY; Schema: public; Owner: postgres
--

ALTER TABLE public.twilio_info ENABLE ROW LEVEL SECURITY;

--
-- PostgreSQL database dump complete
--

