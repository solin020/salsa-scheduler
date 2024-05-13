from fastapi import FastAPI, Request, Response, Depends, UploadFile
from starlette.responses import FileResponse 
from starlette.staticfiles import StaticFiles
from twilio.rest import Client
from database import (Admin, Coordinator, Annotator, Participant, 
    MessageSchedule, MessageResponse, TestPrototype,
    get_db, update_users)
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, text
from datetime import datetime, timezone, timedelta
from uuid import uuid4
import re, aiofiles, os, aiofiles.os, phonenumbers
from config import (frontend_directory,
    account_sid, auth_token, twilio_number)
from dataclasses import dataclass
import dataclasses
import json
from upload_files import (save_message_response,save_annotation,save_test_prototype,
    get_annotation_path,get_message_response_dir_path,get_message_response_file_path,
    get_test_prototype_dir_path,get_test_prototype_file_path,get_test_prototype_zip_path,
    delete_annotation,delete_message_response,delete_test_prototype)
from test_prototype import TestPrototypeMetadata

RETRIES = 3
RETRY_SECONDS = 600
app = FastAPI()
client = Client(account_sid, auth_token)






#region device

@app.post('/salsa/device/api/upload-response-file')
async def device_upload_response_file(schedule_id:str, test_prototype_id:str, upload_zip_pgp: UploadFile, db:AsyncSession=Depends(get_db)):
    if (participant := (await db.exec(
        select(Participant).where(Participant.id==schedule_id)
      )).one_or_none()):
        now = datetime.now(timezone.utc).astimezone()
        await save_message_response(
            participant.projects[0], schedule_id, test_prototype_id, 
            now.isoformat(), participant.id, 
            upload_zip_pgp
        )
        mr = MessageResponse(
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


@app.post('/salsa/server/api/upload-response-file')
async def coordinator_upload_response_file(subject_id:str, schedule_id:str, test_prototype_id:str, upload_zip_pgp: UploadFile, db:AsyncSession=Depends(get_db)):
    if (participant := (await db.exec(
        select(Participant).where(Participant.id==subject_id)
      )).one_or_none()):
        now = datetime.now(timezone.utc).astimezone()
        await save_message_response(
            participant.projects[0], schedule_id, test_prototype_id, 
            now.isoformat(), participant.id, 
            upload_zip_pgp
        )
        mr = MessageResponse(
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

@app.post('/salsa/server/api/delete-admin')
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

@app.post('/salsa/server/api/delete-coordinator')
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

@app.post('/salsa/server/api/delete-annotator')
async def delete_annotator(id:str, project:str, db:AsyncSession=Depends(get_db)):
    if (annotator := (await (db.exec(select(Annotator).where(Annotator.id==id)))).one_or_none()):
        annotator.projects.remove(project)
        if not annotator.projects:
            await db.delete(annotator)
    await db.commit()
    await update_users()



@app.post('/salsa/server/api/add-participant')
async def add_participant(id:str, project:str, phone_number:str, db:AsyncSession=Depends(get_db)):
    pn = phonenumbers.parse(phone_number, "US")
    #this accounts for variability in phone number formatting
    adjusted_pn = f'+{pn.country_code}{pn.national_number}'
    participant = Participant(id=id,phone_number=adjusted_pn, projects=[project])
    db.add(participant)
    await db.commit()
    await update_users()

@app.post('/salsa/server/api/delete-participant')
async def delete_participant(id:str, db:AsyncSession=Depends(get_db)):
    participant = (await (db.exec(select(Participant).where(Participant.id==id)))).one()
    await db.delete(participant)
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


@dataclass
class ApiMessageSchedule:
    project: str
    participant:Participant
    start_date: datetime
    end_date: datetime
    times: list[tuple[int,int]]
    prototype_id: str
@app.post('/salsa/server/api/schedule-messages')
async def coordinator_schedule_messages(s:ApiMessageSchedule, db:AsyncSession=Depends(get_db)):
    for day in range((s.end_date-s.start_date).days+1):
        for hour, minute in s.times:
            print(day,hour,minute)
            time = s.start_date + timedelta(days=day, hours=hour, minutes=minute)
            time = time.astimezone(timezone.utc)
            schedule_id = str(uuid4())
            db.add(MessageSchedule(
                project=s.project,
                tries=0,
                max_tries=1,
                message=f"Respond to prototype {s.prototype_id} with code {schedule_id}",
                source_number=twilio_number,
                participant_id=s.participant.id,
                dest_number=s.participant.phone_number,
                account_sid=account_sid,
                auth_token=auth_token,
                prototype_id=s.prototype_id,
                schedule_id=schedule_id,
                time=time,
                bug_interval=timedelta(minutes=10),
            ))
    await db.commit()



@app.post('/salsa/server/api/delete-messages')
async def coordinator_delete_messages(participant_study_id:str, db:AsyncSession=Depends(get_db)):
    smss = list((await db.exec(
        select(MessageSchedule).where(MessageSchedule.participant_study_id==participant_study_id)
    )).all())
    for sms in smss:
        await db.delete(sms)
    await db.commit()


@app.post('/salsa/server/api/delete-message')
async def coordinator_delete_message(schedule_id:str, db:AsyncSession=Depends(get_db)):
    db_sm = (await db.exec(select(MessageSchedule).where(MessageSchedule.schedule_id==schedule_id))).one()
    await db.delete(db_sm)
    await db.commit()


@app.post('/salsa/server/api/get-messages-and-responses')
async def coordinator_get_messages(participant_id:str, db:AsyncSession=Depends(get_db)) -> tuple[list[MessageSchedule], list[MessageResponse]]:
    smss = list((await db.exec(
        select(MessageSchedule).where(MessageSchedule.participant_id==participant_id)
    )).all())
    responses = list((await db.exec(
        select(MessageResponse).where(MessageResponse.participant_id==participant_id)
    )).all())
    return (smss, responses)

@app.get('/salsa/server/get-message-response-files')
async def get_message_response_files(schedule_id: str, db:AsyncSession=Depends(get_db)) -> list[str]:
    mr = (await db.exec(select(MessageResponse).where(MessageResponse.schedule_id==schedule_id))).one()
    mr_directory = get_message_response_dir_path(mr.project, mr.schedule_id)
    retval = []
    for filename in await aiofiles.os.listdir(mr_directory):
        retval.append(get_message_response_file_path(mr.project, mr.schedule_id, filename))
    return retval

@app.get('/salsa/server/get-message-response-file')
async def get_message_response_file(schedule_id: str, filepath:str, db:AsyncSession=Depends(get_db)):
    mr = (await db.exec(select(MessageResponse).where(MessageResponse.schedule_id==schedule_id))).one()
    mr_path = get_message_response_dir_path(mr.project, mr.schedule_id)
    if mr_path == os.path.dirname(filepath):
        return FileResponse(filepath)
    

@app.get('/salsa/device/get-test-prototype')
async def device_get_test_prototype(id:str, db:AsyncSession=Depends(get_db)) -> FileResponse:
    test_prototype = (await db.exec(select(TestPrototype).where(TestPrototype.id==id))).one()
    return FileResponse(get_test_prototype_zip_path(
        project=test_prototype.project,
        id=test_prototype.id
    ))

@app.get('/salsa/server/get-test-prototypes')
async def coordinator_get_test_prototypes(project:str, db:AsyncSession=Depends(get_db)) -> list[str]:
    return [t.id for t in (
        await db.exec(select(TestPrototype).where(TestPrototype.project==project))
        ).all()]

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
    tp = (await db.exec(select(TestPrototype).where(TestPrototype.id==id))).one()
    tp_path = get_test_prototype_dir_path(tp.project, tp.id)
    if tp_path == os.path.dirname(filepath):
        return FileResponse(filepath)
 
@app.post('/salsa/server/add-test-prototype')
async def add_test_prototype(r:Request, db:AsyncSession=Depends(get_db)):
    params = r.query_params
    project = params['project']
    id = params['id'] 
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
            id=id,
            metadata_json=metadata_json,
            infiles=infiles,
            filenames=filenames,
            replace=replace
        )
    tp = TestPrototype(
        project=project,
        id=id,
    )
    db.add(tp)
    await db.commit()







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
