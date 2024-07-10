from fastapi import FastAPI, Request, Response, Depends, UploadFile
from starlette.responses import FileResponse , StreamingResponse
from fastapi.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.background import BackgroundTask
from twilio.rest import Client
from database import (Admin, Coordinator, Annotator, Participant, 
    MessageSchedule, StimulusResult, TestPrototype, Transcription,
    get_db, update_users, SchedulePrototype, AllGroups,
    TwilioInfo)
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, text
from datetime import datetime, timezone, timedelta
from uuid import uuid4
import re, aiofiles, os, aiofiles.os, phonenumbers
from config import (frontend_directory,
    account_sid, auth_token, twilio_number)
from dataclasses import dataclass
import dataclasses
import datetime as DateTime
import json
from upload_files import (save_message_response, save_message_response_nozip,save_annotation,save_test_prototype,
    get_annotation_path,get_message_response_dir_path,get_message_response_file_path,
    get_test_prototype_dir_path,get_test_prototype_file_path,get_test_prototype_zip_path,
    delete_annotation,delete_message_response,delete_test_prototype,
    make_file_zip)
from test_prototype import TestPrototypeMetadata
from fastapi.middleware.cors import CORSMiddleware

RETRIES = 3
RETRY_SECONDS = 600
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client = Client(account_sid, auth_token)






#region device


@app.post('/salsa/device/api/upload-response-file')
async def device_upload_response_file_nozip(r:Request, db:AsyncSession=Depends(get_db)):
    subject_id = r.headers['salsaid']
    print('subject_id', subject_id, flush=True)
    schedule_id = r.query_params['schedule_id']
    test_prototype_id = r.query_params['test_prototype_id']
    sequence_no = int(r.query_params['sequence_no'])
    real_timestamp = datetime.fromisoformat(r.query_params['timestamp'].replace('Z','+00:00'))
    infiles = []
    names = []
    form = await r.form()
    fname, fbody = list(form.items())[0]
    infiles.append(fbody)
    names.append(fname)
    stimulus_id = fname.split('.')[0] 
    if (participant := (await db.exec(
        select(Participant).where(Participant.id==subject_id)
      )).one_or_none()):
        print('nue', flush=True)
        now = datetime.now(timezone.utc).astimezone()
        await save_message_response_nozip(
            participant.projects[0], schedule_id, test_prototype_id, 
            real_timestamp.isoformat(), participant.id, 
            infiles, names, db
        )
        if sequence_no == -1:
            mr = StimulusResult(
                project=participant.projects[0],
                schedule_id=schedule_id,
                participant_id=participant.id,
                test_prototype_id=test_prototype_id,
                miscellaneous={}, 
                stimulus_id=stimulus_id,
                sequence_no=sequence_no,
                real_timestamp=real_timestamp,
                schedule_prototype_id=participant.schedule_prototype_id
            )
        else:
            print('inparams', test_prototype_id,stimulus_id, participant.id, sequence_no, flush=True)
            mr = (await db.exec(select(StimulusResult)
                .where(StimulusResult.test_prototype_id == test_prototype_id)
                .where(StimulusResult.stimulus_id == stimulus_id)
                .where(StimulusResult.participant_id == participant.id)
                .where(StimulusResult.sequence_no == sequence_no)
            )).one()
            
            mr.quality = '3'
            mr.real_timestamp=real_timestamp
        db.add(mr)
        await db.commit()
        return Response('OK')
    return Response('Invalid response code', status_code=406)
               

@app.post('/salsa/server/api/upload-response-file')
async def coordinator_upload_response_file(subject_id:str, schedule_id:str, test_prototype_id:str, upload_zip_pgp: UploadFile, db:AsyncSession=Depends(get_db)):
    if (participant := (await db.exec(
        select(Participant).where(Participant.id==subject_id)
      )).one_or_none()):
        now = datetime.now(timezone.utc).astimezone()
        await save_message_response(
            participant.projects[0], schedule_id, test_prototype_id, 
            now.isoformat(), participant.id, 
            upload_zip_pgp, db
        )
        mr = StimulusResult(
            project=participant.projects[0],
            schedule_id=schedule_id,
            participant_id=participant.id,
            timestamp=now,
            test_prototype_id=test_prototype_id,
            miscellaneous={}, 
        )
        db.add(mr)
        await db.commit()
        return Response('OK')
    return Response('Invalid response code', status_code=406)



@app.get('/salsa/device/client/client.html')
async def test_get_client():
    return FileResponse(os.path.join(frontend_directory, 'backend/dummyclient.html'))

@app.get('/salsa/device/client/openpgp.js')
async def test_get_openpgp():
    return FileResponse(os.path.join(frontend_directory, 'backend/openpgp.js'))
#endregion
#region coordinator




@app.get('/salsa/server/api/get-your-email')
async def get_your_email(r:Request)->str:
    print('salsaid ')
    return r.headers.get('salsaid')





@app.get('/salsa/server/api/get-admins')
async def get_admins(db:AsyncSession=Depends(get_db)) -> list[str]:
    return [a.id for a in (await db.exec(select(Admin))).all()]

@app.post('/salsa/server/api/add-admin')
async def add_admin(id:str, db:AsyncSession=Depends(get_db)):
    check_valid_username(id)
    admin = Admin(id=id)
    db.add(admin)
    await db.commit()
    await update_users()

@app.delete('/salsa/server/api/delete-admin')
async def delete_admin(id:str, db:AsyncSession=Depends(get_db)):
    print(f"id is |{id}|")
    admin = (await (db.exec(select(Admin).where(Admin.id==id)))).one()
    await db.delete(admin)
    await db.commit()
    await update_users() 


@app.get('/salsa/server/api/get-coordinators')
async def get_coordinators(db:AsyncSession=Depends(get_db)) -> list[Coordinator]:
    return list((await db.exec(select(Coordinator))).all())

@app.post('/salsa/server/api/add-coordinator')
async def add_coordinator(id:str, project:str, db:AsyncSession=Depends(get_db)):
    check_valid_username(id)
    if (coordinator := (await (db.exec(select(Coordinator).where(Coordinator.id==id)))).one_or_none()):
        coordinator.projects.append(project)
    else:
        coordinator = Coordinator(id=id, projects=[project])
    db.add(coordinator)
    await db.commit()
    await update_users()

@app.delete('/salsa/server/api/delete-coordinator')
async def delete_coordinator(id:str, project:str, db:AsyncSession=Depends(get_db)):
    if (coordinator := (await (db.exec(select(Coordinator).where(Coordinator.id==id)))).one_or_none()):
        coordinator.projects.remove(project)
        db.add(coordinator)
        if not coordinator.projects:
            await db.delete(coordinator)
    await db.commit()
    await update_users()

@app.get('/salsa/server/api/get-annotators-admin')
async def get_annotators_admin(db:AsyncSession=Depends(get_db)) -> list[Annotator]:
    return list((await db.exec(select(Annotator))).all())

@app.get('/salsa/server/api/get-annotators')
async def get_annotators(project:str,db:AsyncSession=Depends(get_db)) -> list[str]:
    return [a for a in (await db.exec(select(Annotator)))if project in a.projects]

@app.post('/salsa/server/api/add-annotator')
async def add_annotator(id:str, project:str, db:AsyncSession=Depends(get_db)):
    check_valid_username(id)
    if (annotator := (await (db.exec(select(Annotator).where(Annotator.id==id)))).one_or_none()):
        annotator.projects.append(project)
    else:
        annotator = Coordinator(id=id, projects=[project])
    db.add(annotator)
    await db.commit()
    await update_users()

@app.delete('/salsa/server/api/delete-annotator')
async def delete_annotator(id:str, project:str, db:AsyncSession=Depends(get_db)):
    if (annotator := (await (db.exec(select(Annotator).where(Annotator.id==id)))).one_or_none()):
        annotator.projects.remove(project)
        if not annotator.projects:
            await db.delete(annotator)
    await db.commit()
    await update_users()

           

@app.post('/salsa/server/api/add-participant')
async def add_participant(r:Request, id:str, project:str, phone_number:str, schedule_prototype_id:str, twilio_nickname:str, db:AsyncSession=Depends(get_db)):
    pn = phonenumbers.parse(phone_number, "US")
    #this accounts for variability in phone number formatting
    adjusted_pn = f'+{pn.country_code}{pn.national_number}'
    participant = Participant(
        id=id,
        phone_number=adjusted_pn, 
        projects=[project],
        dropout=False,
        schedule_prototype_id=schedule_prototype_id,
        schedule = await r.json(),
        twilio_nickname=twilio_nickname)
    db.add(participant)
    await db.commit()
    await update_users()

@app.patch('/salsa/server/api/drop-participant')
async def delete_participant(id:str, db:AsyncSession=Depends(get_db)):
    participant = (await (db.exec(select(Participant).where(Participant.id==id)))).one()
    participant.dropout = True
    db.add(participant)
    await db.commit()

@app.get('/salsa/server/api/get-participants-admin')
async def get_participants_admin(db:AsyncSession=Depends(get_db)) -> list[Participant]:
    return list((await db.exec(select(Participant))).all())

@app.get('/salsa/server/api/get-participants')
async def get_participant(project:str,db:AsyncSession=Depends(get_db)) -> list[Participant]:
    return [p for p in (await db.exec(select(Participant)))if project in p.projects]




@app.get('/salsa/server/api/coordinator-get-projects')
async def coordinator_get_projects(db:AsyncSession=Depends(get_db)) -> list[str]:
    return (await db.exec(select(Coordinator))).one().projects

@app.get('/salsa/server/api/admin-get-projects')
async def admin_get_projects(db:AsyncSession=Depends(get_db)) -> list[str]:
    return sum([p.projects for p in (await db.exec(select(Coordinator))).all()],[])

@app.get('/salsa/server/api/annotator-get-projects')
async def annotator_get_projects(db:AsyncSession=Depends(get_db)) -> list[str]:
    return (await db.exec(select(Annotator))).one().projects



@app.get('/salsa/server/api/get-twilio-info')
async def get_twilio_info(project:str, db:AsyncSession=Depends(get_db))->list[TwilioInfo]:
    return list((await db.exec(select(TwilioInfo).where(TwilioInfo.project==project))).all())

@app.post('/salsa/server/api/add-twilio-info')
async def add_twilio_info(project:str, nickname:str, account_sid:str, auth_token:str, phone_number:str, db:AsyncSession=Depends(get_db)):
    if (existing_twilio_info := (await db.exec(select(TwilioInfo).where(TwilioInfo.nickname==nickname))).one_or_none()):
        existing_twilio_info.account_sid = account_sid
        existing_twilio_info.auth_token = auth_token
        existing_twilio_info.phone_number = phone_number
        db.add(existing_twilio_info)
    else:
        db.add(TwilioInfo(
            nickname=nickname,
            project=project,
            account_sid=account_sid,
            auth_token=auth_token,
            phone_number=phone_number
        ))
    await db.commit()

@app.delete('/salsa/server/api/delete-twilio-info')
async def delete_twilio_info(project:str, account_sid:str, auth_token:str, phone_number:str, db:AsyncSession=Depends(get_db)):
    infos = list((await db.exec(select(TwilioInfo).where(
            TwilioInfo.project==project
        ).where(
            TwilioInfo.account_sid==account_sid
        ).where(
            TwilioInfo.auth_token==auth_token
        ).where(
            TwilioInfo.phone_number==phone_number
        ))).all())
    for info in infos:
        await db.delete(info)
    await db.commit()


@app.post('/salsa/server/api/schedule-messages')
async def coordinator_schedule_messages(r:Request, db:AsyncSession=Depends(get_db)):
    pass







@app.post('/salsa/server/api/get-messages-and-responses')
async def coordinator_get_messages(participant_id:str, db:AsyncSession=Depends(get_db)) -> tuple[list[MessageSchedule], list[StimulusResult]]:
    smss = list((await db.exec(
        select(MessageSchedule).where(MessageSchedule.participant_id==participant_id)
    )).all())
    responses = list((await db.exec(
        select(StimulusResult).where(StimulusResult.participant_id==participant_id)
    )).all())
    return (smss, responses)




@app.get('/salsa/server/get-project-message-response-files')
async def get_message_response_files(project: str, db:AsyncSession=Depends(get_db)) -> Response:
    mrs = (await db.exec(select(StimulusResult).where(StimulusResult.project==project))).all()
    fnames = set()
    for mr in mrs:
        mr_directory = get_message_response_dir_path(mr.project, mr.schedule_id)
        for filename in await aiofiles.os.listdir(mr_directory):
            fnames.add((mr.schedule_id, get_message_response_file_path(mr.project, mr.schedule_id, filename)))
    return StreamingResponse(
        content=await make_file_zip(list(fnames)), 
        headers={"Content-disposition":f'''attachment; filename="{project}.zip"'''},
        media_type="application/zip"
    )


@app.get('/salsa/server/get-participant-message-response-files')
async def get_message_response_files(participant_id: str, db:AsyncSession=Depends(get_db)) -> Response:
    mrs = (await db.exec(select(StimulusResult).where(StimulusResult.participant_id==participant_id))).all()
    fnames = set()
    for mr in mrs:
        mr_directory = get_message_response_dir_path(mr.project, mr.schedule_id)
        for filename in await aiofiles.os.listdir(mr_directory):
            fnames.add((mr.schedule_id, get_message_response_file_path(mr.project, mr.schedule_id, filename)))
        return StreamingResponse(
        content=await make_file_zip(list(fnames)), 
        headers={"Content-disposition":f'''attachment; filename="{participant_id}.zip"'''},
        media_type="application/zip"
    )

@app.get('/salsa/server/get-message-response-files')
async def get_message_response_files(schedule_id: str, db:AsyncSession=Depends(get_db)) -> list[str]:
    mrs = (await db.exec(select(StimulusResult).where(StimulusResult.schedule_id==schedule_id))).all()
    mr_directory = get_message_response_dir_path(mrs[0].project, mrs[0].schedule_id)
    retval = set()
    for mr in mrs:
        for filename in await aiofiles.os.listdir(mr_directory):
            retval.add(get_message_response_file_path(mr.project, mr.schedule_id, filename))
    return list(retval)

@app.get('/salsa/server/get-message-response-file')
async def get_message_response_file(schedule_id: str, filepath:str, db:AsyncSession=Depends(get_db)):
    mrs = (await db.exec(select(StimulusResult).where(StimulusResult.schedule_id==schedule_id))).all()
    mr_path = get_message_response_dir_path(mrs[0].project, mrs[0].schedule_id)
    if mr_path == os.path.dirname(filepath):
        return FileResponse(filepath)

@app.get('/salsa/server/get-message-response-transcriptions')
async def get_message_response_transcriptions(schedule_id:str, db:AsyncSession=Depends(get_db)) -> list[Transcription]:
    return (await db.exec(select(Transcription).where(Transcription.schedule_id==schedule_id))).all()
    

@app.get('/salsa/device/get-test-prototype')
async def device_get_test_prototype(id:str, db:AsyncSession=Depends(get_db)) -> FileResponse:
    test_prototype = (await db.exec(select(TestPrototype).where(TestPrototype.id==id))).one()
    return FileResponse(get_test_prototype_zip_path(
        project=test_prototype.project,
        id=test_prototype.id
    ))
 
     
@app.get('/salsa/device/get-schedule')
async def device_get_schedule(r: Request, db:AsyncSession=Depends(get_db)):
    participant_id = r.headers['salsaid']
    print('get schedule', flush=True)
    schedule = (await db.exec(select(Participant).where(Participant.id==participant_id))).one().schedule
    return JSONResponse(schedule)
      
      
@app.get('/salsa/server/api/get-schedules')
async def get_schedules(project:str, db:AsyncSession=Depends(get_db)):
    print('got to schedule')   
    return JSONResponse(list((await db.exec(select(SchedulePrototype.schedule).where(SchedulePrototype.project==project))).all()))

@app.post('/salsa/server/api/add-schedule')
async def add_schedule(r: Request, project:str, id:str, db:AsyncSession=Depends(get_db)):
    db.add(
        SchedulePrototype(
            project=project,
            id=id,
            schedule=await r.json()
        )
    )
    await db.commit()





@app.get('/salsa/server/get-test-prototypes')
async def coordinator_get_test_prototypes(project:str, db:AsyncSession=Depends(get_db))->list:
    retval = []
    for tp in (await (db.exec(select(TestPrototype).where(TestPrototype.project==project)))).all():
        async with aiofiles.open(get_test_prototype_file_path(tp.project, tp.id, 'metadata.json')) as f:
            metadata = json.loads(await f.read())
            response_stimuli = []
            for m in metadata:
                if m['type'] in ('recording', 'ema'):
                    response_stimuli.append(m['id'])
            retval.append(
                {'id':tp.id, 'project':tp.project, 'groups':tp.groups, 'response_stimuli':response_stimuli}
            )
    return retval


@app.get('/salsa/server/get-test-prototype-files')
async def get_test_prototype_files(id: str, db:AsyncSession=Depends(get_db)) -> list[str]:
    tp = (await db.exec(select(TestPrototype).where(TestPrototype.id==id))).one()
    tp_directory = get_test_prototype_dir_path(tp.project, tp.id)
    retval = []
    for filename in await aiofiles.os.listdir(tp_directory):
        retval.append(get_test_prototype_file_path(tp.project, tp.id, filename))
    return retval

@app.get('/salsa/server/get-test-prototype-file')
async def get_test_prototype_file(id: str, filepath:str, db:AsyncSession=Depends(get_db)):
    print('got to here', flush=True)
    tp = (await db.exec(select(TestPrototype).where(TestPrototype.id==id))).one()
    tp_path = get_test_prototype_dir_path(tp.project, tp.id)
    if tp_path == os.path.dirname(filepath):
        return FileResponse(filepath)
 
@app.post('/salsa/server/add-test-prototype')
async def add_test_prototype(r:Request, db:AsyncSession=Depends(get_db)):
    print('added test prototype', flush=True)
    params = r.query_params
    project = params['project']
    id = params['id'] 
    groups:list[str] = json.loads(params['groups'])
    replace = False
    if (tp:=(await db.exec(select(TestPrototype).where(TestPrototype.project==project).where(TestPrototype.id==id))).one_or_none()):
        print('replaced', id)
        replace=True
        await db.delete(tp)
        await db.commit()
    filenames = []
    infiles = []
    async with r.form() as form:
        fdict = {}
        for k, v in form.items():
            fdict[k] = v
        metadata_json=fdict.pop('metadata.json')
        for k, v in fdict.items():
            filenames.append(k)
            infiles.append(v)
        await save_test_prototype(
            project=project,
            id_=id,
            metadata_json=metadata_json,
            infiles=infiles,
            filenames=filenames,
            replace=replace
        )
    tp = TestPrototype(
        project=project,
        id=id,
        groups=groups
    )
    db.add(tp)
    await db.commit()


@app.get('/salsa/server/api/get-groups')
async def get_groups(project:str, db:AsyncSession=Depends(get_db))->list[str]:
    return [g.group for g in (await db.exec(select(AllGroups).where(AllGroups.project==project))).all()]

@app.get('/salsa/server/api/get-dashboard-data')
async def get_dashboard_data(project:str, schedule_prototype_id:str, db:AsyncSession=Depends(get_db)):
    retval = []
    for s in (await db.exec(select(StimulusResult)
        .where(StimulusResult.project==project)
        .where(StimulusResult.schedule_prototype_id==schedule_prototype_id)
    )).all():
        retval.append({
            'participant_id': s.participant_id,
            'stimulus_id':s.stimulus_id,
            'quality':int(s.quality),
            'sequence_no':s.sequence_no,
            'schedule_id':s.schedule_id,
            'test_prototype_id':s.test_prototype_id,
            'formal_timestamp':s.formal_timestamp,
            'real_timestamp':s.real_timestamp
        })
    return retval






def check_valid_username(s):
    assert re.match('\A[a-zA-Z0-9_.@]+\Z', s), "Invalid username"

def check_valid_project(s):
    assert re.match('\A[a-zA-Z0-9_.@ ]+\Z', s), "Invalid username"




@app.get("/salsa/server/public.pgp",)
async def read_public_key():
    return FileResponse(os.path.join(frontend_directory, 'public/public.pgp'))


@app.get("/salsa/server/coordinator.html",)
async def read_coordinator():
    return FileResponse(os.path.join(frontend_directory, 'dist/coordinator.html'))

@app.get("/salsa/server/annotator.html",)
async def read_annotator():
    return FileResponse(os.path.join(frontend_directory, 'dist/annotator.html'))
 
@app.get("/salsa/server/admin.html",)
async def read_admin():
    return FileResponse(os.path.join(frontend_directory, 'dist/admin.html'))

app.mount("/salsa/server/assets", StaticFiles(directory=os.path.join(frontend_directory, 'dist/assets')), name="dist")

#endregion 
