--
-- Name: send_twilio_sms(text, text, text, integer, text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.send_twilio_sms(twilio_nickname text, dest_number text, message text, tries integer, participant_id text) RETURNS integer
    LANGUAGE plpython3u
    AS $_$
from twilio.rest import Client
try:
	if "sms_participant_plan" not in SD:
	    sms_participant_plan = plpy.prepare("SELECT * from participants WHERE id=$1", ["text"])
	    SD["sms_participant_plan"] = sms_participant_plan
	else:
	    sms_participant_plan = SD['sms_participant_plan']
	    
	participant = sms_participant_plan.execute([participant_id])[0]
	if participant['dropout']:
		return tries + 1

	if "twilio_info_plan" not in SD:
	    twilio_info_plan = plpy.prepare("SELECT * FROM twilio_info WHERE nickname=$1", ["text"])
	    SD["twilio_info_plan"] = twilio_info_plan
	else:
	    twilio_info_plan = SD['twilio_info_plan']

	twilio_info = twilio_info_plan.execute([twilio_nickname])[0]
	client = Client(twilio_info["account_sid"], twilio_info["auth_token"])
	client.messages.create(
		to=dest_number,
		from_=twilio_info["phone_number"],
		body=message
	)
	return tries + 1
except:
	pass
$_$;


ALTER FUNCTION public.send_twilio_sms(twilio_nickname text, dest_number text, message text, tries integer, participant_id text) OWNER TO postgres;
