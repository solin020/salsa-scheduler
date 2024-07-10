from fastapi import UploadFile
import os
from config import message_response_directory, gpg_phassphrase, test_prototype_directory, annotation_directory
import aiofiles, asyncio
import aiofiles.os
import aiohttp
from sqlmodel.ext.asyncio.session import AsyncSession
from database import Transcription
import json
from uuid import uuid4


async def save_message_response(project: str, 
                                schedule_id:str,  
                                test_prototype_id: str, 
                                datestr:str, 
                                subject_id:str, 
                                infile: UploadFile,
                                db:AsyncSession):
    print('uploading response', flush=True)
    project_directory = os.path.join(message_response_directory, project)
    if not os.path.exists(project_directory):
        os.mkdir(project_directory)
    final_destination = os.path.join(project_directory, schedule_id)
    command = f'''mkdir -p "{final_destination}"'''
    await (await asyncio.create_subprocess_shell(command)).wait()
    gpg_destination = final_destination + ".gpg"
    zip_destination = final_destination + ".zip"
    async with aiofiles.open(gpg_destination, 'wb+') as gpg_f:
        await gpg_f.write(await infile.read())
    command = (f'''gpg  --no-tty --pinentry-mode=loopback --passphrase "{gpg_phassphrase}" '''
               f''' -d -o "{zip_destination}" "{gpg_destination}" ;'''
               f''' rm "{gpg_destination}" ;'''
               f''' unzip  -d "{final_destination}" -j "{zip_destination}";'''
               f''' rm "{zip_destination}" ''')

    await (await asyncio.create_subprocess_shell(command)).wait()
    prefix = f'project={project}&subject_id={subject_id}&test_prototype_id={test_prototype_id}&date={datestr}&file='
    print('got to filenames', flush=True)
    filenames = await aiofiles.os.listdir(final_destination)
    for filename in filenames:
        print(os.path.join(final_destination, filename), os.path.join(final_destination, f'{prefix}_{filename}'), flush=True)
        fullname = os.path.join(final_destination, filename)
        command = f"""ffprobe -loglevel error -show_entries stream=codec_type -of default=nw=1 '{fullname}'"""
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        audiocheck, stderr = await proc.communicate()
        print('audiocheck', audiocheck, stderr, flush=True)
        if b'audio' in audiocheck:
            totranscribe_filename = fullname + '_totranscribe.wav'
            command = f"""ffmpeg -i '{fullname}' -acodec pcm_s16le -ar 16000 -ac 1 '{totranscribe_filename}'"""
            await (await asyncio.create_subprocess_shell(command)).wait()
            async with aiofiles.open(totranscribe_filename, 'rb') as f:
                async with aiohttp.ClientSession() as session:
                    async with session.post(f'http://salsa2_whisperx:9876/process-bytes', data=(await f.read())[42:]) as resp:
                        name = filename.split('.')[0]
                        db.add(
                            Transcription(
                                project=project,
                                schedule_id=schedule_id,
                                segments=convert_to_scription(json.loads(await resp.json()), filename),
                                score=0,
                                stimulus_id=name
                            )
                        )  

        await aiofiles.os.rename(os.path.join(final_destination, filename), os.path.join(final_destination, f'{prefix}_{filename}'))
    await db.commit()


async def save_message_response_nozip(project: str, 
                                schedule_id:str,  
                                test_prototype_id: str, 
                                datestr:str, 
                                subject_id:str, 
                                infiles: list[UploadFile],
                                names: list[str],
                                db:AsyncSession):
    print('uploading response', flush=True)
    cwd = os.getcwd()
    project_directory = os.path.join(message_response_directory, project)
    if not os.path.exists(project_directory):
        os.mkdir(project_directory)
    final_destination = os.path.join(project_directory, schedule_id)
    command = f'''mkdir -p "{final_destination}"'''
    await (await asyncio.create_subprocess_shell(command)).wait()
    os.chdir(final_destination)
    for infile, name in zip(infiles, names):
        gpg_destination = name
        filename = gpg_destination[:-4]
        print('gpg_destination', gpg_destination, flush=True)
        prefix = f'project={project}&subject_id={subject_id}&test_prototype_id={test_prototype_id}&date={datestr}&file='
        fullname = prefix + filename
        async with aiofiles.open(gpg_destination, 'wb+') as gpg_f:
            await gpg_f.write(await infile.read())
        command = (f'''gpg --no-tty --pinentry-mode=loopback --passphrase "{gpg_phassphrase}" '''
                   f''' -d -o "{fullname}" "{gpg_destination}" ;'''
                   f''' rm "{gpg_destination}" ;''')
        await (await asyncio.create_subprocess_shell(command)).wait()
        command = f"""ffprobe -loglevel error -show_entries stream=codec_type -of default=nw=1 '{fullname}'"""
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        audiocheck, stderr = await proc.communicate()
        print('audiocheck', infile, audiocheck, stderr, flush=True)
        if b'audio' in audiocheck:
            totranscribe_filename = fullname + '_totranscribe.wav'
            print('attempting transcription')
            command = f"""ffmpeg -i '{fullname}' -acodec pcm_s16le -ar 16000 -ac 1 '{totranscribe_filename}'"""
            await (await asyncio.create_subprocess_shell(command)).wait()
            async with aiofiles.open(totranscribe_filename, 'rb') as f:
                async with aiohttp.ClientSession() as session:
                    async with session.post(f'http://salsa2_whisperx:9876/process-bytes', data=(await f.read())[42:]) as resp:
                        print('transcription finished')
                        name = filename.split('.')[0]
                        db.add(
                            Transcription(
                                project=project,
                                schedule_id=schedule_id,
                                segments=json.loads(await resp.json()),
                                score=0,
                                stimulus_id=name
                            )
                        )  
    await db.commit()
    os.chdir(cwd)


def get_message_response_dir_path(project, schedule_id):
    return os.path.join(message_response_directory, project, schedule_id)

def get_message_response_file_path(project, schedule_id, filename):
    return os.path.join(message_response_directory, project, schedule_id, filename)

async def delete_message_response(project, schedule_id):
    await aiofiles.os.rmdir(get_message_response_dir_path(project, schedule_id))
 


async def save_annotation(project: str, schedule_id:str,  filename:str, infile: UploadFile):
    project_directory = os.path.join(annotation_directory, project)
    if not os.path.exists(project_directory):
        os.mkdir(project_directory)
    final_destination = os.path.join(project_directory, schedule_id)
    if not os.path.exists(final_destination):
        os.mkdir(final_destination)
    true_path = os.path.join(final_destination, filename)
    async with aiofiles.open(true_path, 'wb+') as f:
        await f.write(await infile.read())

def get_annotation_path(project: str, schedule_id:str,  filename:str):
    return os.path.join(annotation_directory, project, schedule_id, filename)

async def delete_annotation(project: str, schedule_id:str,  filename:str):
    dir_path = os.path.join(annotation_directory, project, schedule_id, filename)
    command = f'''rm -rf {dir_path}'''
    await (await asyncio.create_subprocess_shell(command)).wait()



async def save_test_prototype(project:str, id_:str, metadata_json:str, infiles: list[UploadFile], filenames:list[str], replace=False):
    cwd = os.getcwd()
    project_directory = os.path.join(test_prototype_directory, project)
    if not os.path.exists(project_directory):
        await aiofiles.os.mkdir(project_directory)  
    os.chdir(project_directory)
    true_path = id_
    true_zip = id_ + '.zip'  
    if replace:
        command = f''' rm -rf {true_path}; rm {true_zip} '''
        await (await asyncio.create_subprocess_shell(command)).wait()
    if not os.path.exists(true_path):
        await aiofiles.os.mkdir(true_path)
    for infile, filename in zip(infiles, filenames):
        fpath = os.path.join(true_path, filename)
        print('saving filename')
        async with aiofiles.open(fpath, 'wb+') as f:
            await f.write(await infile.read()) 
        async with aiofiles.open(os.path.join(true_path, 'metadata.json'), 'w+') as f:
            await f.write(metadata_json) 
    command = f'''zip -r {true_zip} {true_path} '''
    await (await asyncio.create_subprocess_shell(command)).wait()
    os.chdir(cwd)

def get_test_prototype_zip_path(project: str, id:str):
    return os.path.join(test_prototype_directory, project, id+'.zip')

def get_test_prototype_dir_path(project: str, id:str):
    return os.path.join(test_prototype_directory, project, id)

def get_test_prototype_file_path(project: str, id:str, filename:str):
    return os.path.join(test_prototype_directory, project, id, filename)


async def delete_test_prototype(project: str, id:str):
    dir_path = get_test_prototype_dir_path(project, id)
    zip_path = get_test_prototype_zip_path(project, id)
    await aiofiles.os.remove(zip_path)
    command = f'''rm -rf {dir_path}'''
    await (await asyncio.create_subprocess_shell(command)).wait()


def convert_to_scription(transcription: dict, name:str):
    return {
        'annotator': '',
        'revision': '',
        'filename': name,
        'results': {
            'transcripts':[' '.join(t['text'] for t in transcription['segments'])],
            'speakers': {
                'speakers': 1,
                'segments': [
                    {
                        'start_time': str(t['start']),
                        'end_time': str(t['end']),
                        'speaker_label': 'spk_0',
                        'items': [
                            {
                                'start_time': str(w['start']),
                                'end_time': str(w['end']),
                                'speaker_label': 'spk_0'
                            } for w in t['words']
                        ]
                    } for t in transcription['segments']
                ]
            },
            'items': [
                {
                    'start_time': str(w['start']),
                    'end_time': str(w['end']),
                    'type': 'pronounciation',
                    'alternatives': {
                        'confidence': str(w['score']),
                        'content': w['word']
                    }

                } for t in transcription['segments'] for w in t['words']],
        },
    }

async def make_file_zip(files:tuple[str,str])->bytes:
    cwd = os.getcwd()
    id = str(uuid4())
    download_directory = os.path.join(message_response_directory, id)
    zip_location = os.path.join(message_response_directory, f'{id}.zip')
    if not os.path.exists(download_directory):
        await aiofiles.os.mkdir(download_directory)  
    os.chdir(download_directory)
    for sid, fname in files:
        command = f'''cp '{fname}' '{download_directory}/{sid}|{fname.split('/')[-1]}' '''
        await (await asyncio.create_subprocess_shell(command)).wait()
    command = f'''zip -r {zip_location} . '''
    print('zipcommand', command)
    await (await asyncio.create_subprocess_shell(command)).wait()
    os.chdir(cwd)
    async def iterfile():
       async with aiofiles.open(zip_location, 'rb') as f:
            while chunk := await f.read(2**10):
                yield chunk
            command = f'''rm -rf {download_directory}; rm -rf {zip_location}'''
            await (await asyncio.create_subprocess_shell(command)).wait()
            yield b''
    return iterfile()

