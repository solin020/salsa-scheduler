from fastapi import UploadFile
import os
from config import message_response_directory, gpg_phassphrase, test_prototype_directory, annotation_directory
import aiofiles, asyncio
import aiofiles.os

async def save_message_response(project: str, schedule_id:str,  test_prototype_id: str, datestr:str, subject_id:str, infile: UploadFile):
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
    command = (f'''gpg --pinentry-mode=loopback --passphrase "{gpg_phassphrase}" '''
               f''' -d -o "{zip_destination}" "{gpg_destination}" ;'''
               f''' rm "{gpg_destination}" ;'''
               f''' unzip  -d "{final_destination}" -j "{zip_destination}";'''
               f''' rm "{zip_destination}" ''')

    await (await asyncio.create_subprocess_shell(command)).wait()
    prefix = f'project={project}&subject_id={subject_id}&test_prototype_id={test_prototype_id}&date={datestr}&file='
    for filename in await aiofiles.os.listdir(final_destination):
        print(os.path.join(final_destination, filename), os.path.join(final_destination, f'{prefix}_{filename}'))
        await aiofiles.os.rename(os.path.join(final_destination, filename), os.path.join(final_destination, f'{prefix}_{filename}'))

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



async def save_test_prototype(project:str, id:str, metadata_json:str, infiles: list[UploadFile], filenames:list[str], replace=False):
    project_directory = os.path.join(test_prototype_directory, project)
    if not os.path.exists(project_directory):
        await aiofiles.os.mkdir(project_directory)  
    true_path = os.path.join(project_directory,  id)
    true_zip = true_path + '.zip'  
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
    command = f'''zip {true_zip} {true_path} '''
    await (await asyncio.create_subprocess_shell(command)).wait()


    await (await asyncio.create_subprocess_shell(command)).wait()

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
