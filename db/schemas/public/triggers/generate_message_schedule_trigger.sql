--
-- Name: participants generate_message_schedule; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER generate_message_schedule AFTER INSERT ON public.participants FOR EACH ROW EXECUTE FUNCTION public.generate_message_schedule_tfn();
