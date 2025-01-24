--
-- Name: generate_message_schedule(text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.generate_message_schedule(participant_id text) RETURNS void
    LANGUAGE plpython3u
    AS $_$ 
import json
if "select_participant" in SD:
    select_participant_plan = SD["select_participant"]
else:
    select_participant_plan = plpy.prepare("SELECT * from participants WHERE id=$1", ["text"])
    SD["select_participant"] = select_participant_plan
pi_info = select_participant_plan.execute([participant_id])[0]
parsed_schedule = json.loads(pi_info["schedule"])
if "message_insert" in SD:
    insert_plan = SD["message_insert"]
else:
    insert_plan = plpy.prepare(
        "INSERT INTO message_schedule"
        "(tries, time, dest_number, message, max_tries, bug_interval, project, test_prototype_id, participant_id, sequence_no, twilio_info, condition) "
        " VALUES (0, $1::timestamptz, $2, $3, 1, $10::interval, $4, $5, $6, $7, $8, $9)", 
        ['text','text','text','text','text','text','integer','text', 'text', 'text'])
    SD["message_insert"] = insert_plan
if "response_insert" in SD:
    response_plan = SD["response_insert"]
else:
    response_plan = plpy.prepare("INSERT INTO stimulus_result"
        "(project, participant_id, formal_timestamp, real_timestamp, test_prototype_id, schedule_id, schedule_prototype_id, stimulus_id, sequence_no, quality)"
        " VALUES ($1, $2, $3::timestamptz, NULL, $4, 'future', $5, $6, $7, '0')", 
        ['text','text','text','text','text','text','integer'])
    SD["response_insert"] = response_plan
for p_idx, phase in enumerate(parsed_schedule['phases']):
    for idx, test in enumerate(phase['spec']['tests']):
        insert_plan.execute([test['formal_timestamp'], 
		pi_info['phone_number'], 
		'''You are due for a SALSA check-in today. Please open the application and follow the instructions to complete your check-in. Reply STOP if you no longer want to receive these notifications.''',  pi_info['projects'][0], 
	        test['prototype_selection']['test_prototype_id'], 
		participant_id, 
		test['sequence_no'], 
		pi_info['twilio_nickname'], 
		'unconditional', 
		'0'])
        insert_plan.execute([test['formal_timestamp'], 
		pi_info['phone_number'], 
		'''Oops ... we haven’t received your response to the latest check-in! Have you uploaded your responses? Please open the SALSA app and complete the check-in to stay on track with the study. Thank you! Reply STOP if you no longer want to receive these notifications.''',  
		pi_info['projects'][0], 
		test['prototype_selection']['test_prototype_id'], 
		participant_id, 
		test['sequence_no'], 
		pi_info['twilio_nickname'], 
		'incomplete',
		'1 day'])
        if idx < len(phase['spec']['tests']) - 1: insert_plan.execute([test['formal_timestamp'], 
		pi_info['phone_number'], 
		'''Thank you for completing your SALSA check-in! In a few days, you will receive another invitation to complete the next check-in. Reply STOP if you no longer want to receive these notifications.''',  pi_info['projects'][0], 
		test['prototype_selection']['test_prototype_id'], 
		participant_id, 
		test['sequence_no'],
	       	pi_info['twilio_nickname'],
	       	'complete', 
		'1 day'])
        if idx==0 and phase['id'] != 'beginning': insert_plan.execute([test['formal_timestamp'], 
		pi_info['phone_number'], 
		'''Reminder: You have a check-in starting soon. Expect a message tomorrow reminding you to complete your check-in in the SALSA app. Reply STOP if you no longer want to receive these notifications.''',  pi_info['projects'][0], 
		test['prototype_selection']['test_prototype_id'], 
		participant_id, 
		test['sequence_no'], 
		pi_info['twilio_nickname'], 
		'unconditional', 
		'-1 day'])
        for stimulus in test['response_stimuli']:
            response_plan.execute([pi_info['projects'][0], participant_id, test['formal_timestamp'],  test['prototype_selection']['test_prototype_id'], pi_info['schedule_prototype_id'],  stimulus['id'], test['sequence_no']])
    if p_idx >= len(parsed_schedule['phases']) - 1: break
    insert_plan.execute([test['formal_timestamp'], 
	pi_info['phone_number'], 
	'''Thank you for completing your SALSA check in! In three months, we will alert you when your next check-in is about to begin. Reply STOP if you no longer want to receive these notifications.''',  
	pi_info['projects'][0], 
	test['prototype_selection']['test_prototype_id'], 
	participant_id, 
	test['sequence_no'], 
	pi_info['twilio_nickname'], 
	'complete', 
	'1 day'])
insert_plan.execute([test['formal_timestamp'], 
	pi_info['phone_number'], 
	'''Thank you for completing your SALSA check in! You are all done with the study! Reply STOP if you no longer want to receive these notifications.''',  
	pi_info['projects'][0], 
	test['prototype_selection']['test_prototype_id'], 
	participant_id, 
	test['sequence_no'], 
	pi_info['twilio_nickname'], 
	'complete', 
	'1 day'])

$_$;


ALTER FUNCTION public.generate_message_schedule(participant_id text) OWNER TO postgres;