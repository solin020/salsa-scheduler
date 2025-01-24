--
-- Name: execute_message_schedule(); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.execute_message_schedule()
    LANGUAGE plpgsql
    AS $$
  BEGIN
	UPDATE message_schedule M 
	  SET tries = send_twilio_sms(M.twilio_info, M.dest_number, M.message, M.tries, M.participant_id) 
	  WHERE ((M.time + M.bug_interval - now()) < (interval '1 minute 30 seconds')) 
	    AND ((M.time + M.bug_interval - now()) > (interval '-1 minute 30 seconds'))
	    AND ((M.condition='unconditional')  
	        OR (M.condition='complete' AND EXISTS (SELECT * FROM stimulus_result S WHERE S.participant_id=M.participant_id AND S.sequence_no=M.sequence_no AND S.quality='3'))
	        OR (M.condition='incomplete' AND NOT EXISTS (SELECT * FROM stimulus_result S WHERE S.participant_id=M.participant_id AND S.sequence_no=M.sequence_no AND S.quality='3')))
	    AND M.tries < M.max_tries 
	    AND M.twilio_info;
  END;

$$;

ALTER PROCEDURE public.execute_message_schedule() OWNER TO postgres;
