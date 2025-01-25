--
-- Name: generate_message_schedule(text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE OR REPLACE FUNCTION public.generate_message_schedule(participant_id text) RETURNS void
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

def get_associated_messages(parsed_schedule, phase, entry):
	base_a = parsed_schedule.get('associated_messages', None)
	phase_a = phase.get('associated_messages', None)
	entry_a = entry.get('associated_messages', None)
	if entry_a and entry_a['type'] != 'none':
		if entry_a['type'] == 'fixed':
			return entry_a['messages']
		else:
			if phase_a and phase_a['type'] != 'none':
				if phase_a['type'] == 'fixed':
					return phase_a['messages']
				else:
					if base_a and base_a['type'] == 'fixed':
						return base_a['messages']
for p_idx, phase in enumerate(parsed_schedule['phases']):
	for idx, test in enumerate(phase['spec']['tests']):
		messages = get_associated_messages(parsed_schedule, phase, test)
		if messages:
			for message in messages:
				insert_plan.execute([test['formal_timestamp'], 
				pi_info['phone_number'], 
				message['message'],  pi_info['projects'][0], 
					test['prototype_selection']['test_prototype_id'], 
				participant_id, 
				test['sequence_no'], 
				pi_info['twilio_nickname'], 
				message['condition'], 
				f'{message["interval"]["count"]} {message["interval"]["unit"]}'])
$_$;


ALTER FUNCTION public.generate_message_schedule(participant_id text) OWNER TO salsa_root;