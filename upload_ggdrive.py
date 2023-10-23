#====Custom package====#
import utils

#====System package====#
import argparse
import os.path

#====3rd package====#
from pydrive.auth import GoogleAuth 
from pydrive.drive import GoogleDrive

ROOT_FOLDER_ID="YOUR_ROOT_FOLDER"

############################################################################################

def fun_connect_gg_drive() -> GoogleDrive:
    credentials_saved = "credentials.json"
    gg_auth = GoogleAuth()
    gg_auth.LoadCredentialsFile(credentials_saved)
    if gg_auth.credentials is None:
        gg_auth.LocalWebserverAuth()
    elif gg_auth.access_token_expired:
        gg_auth.Refresh()
    else:
        gg_auth.Authorize()

    gg_drive = GoogleDrive(gg_auth)
    gg_auth.SaveCredentialsFile(credentials_saved)
    return gg_drive

############################################################################################

def fun_upload_to_drive(gg_drive: GoogleDrive, src: str, dest: str) -> tuple[str, str]:
    seperate_path = dest.split("/")
    folders_name = seperate_path[:-1]
    file_name = seperate_path[-1]
    parent_folder_id = ROOT_FOLDER_ID
    parent_folder_name = "BUILDS"
    for folder_name in folders_name:
        folder_list = gg_drive.ListFile({"q": "title='" + folder_name + "' and '" + parent_folder_id + "' in parents and " + "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
        if not folder_list:
            # Folder in drive not exist, create new
            folder = gg_drive.CreateFile({'title' : folder_name, 'mimeType' : 'application/vnd.google-apps.folder', 'parents': [{'id': parent_folder_id}]})
            folder.Upload()
            utils.ColorPrint(utils.Colors.GREEN, f"Create new folder: name={folder_name} - id={folder['id']}")
            parent_folder_id = folder['id']
            parent_folder_name = folder['title']
        else:
            # Folder in drive exist
            utils.ColorPrint(utils.Colors.WHITE, f"Get existing folder: name={folder_list[0]['title']} - id={folder_list[0]['id']}")
            parent_folder_id = folder_list[0]['id']
            parent_folder_name = folder_list[0]['title']
    
    # Delete existing files have same name
    file_list = gg_drive.ListFile({"q": "title='" + file_name + "' and '" + parent_folder_id + "' in parents and trashed=false"}).GetList()
    for file in file_list:
        utils.ColorPrint(utils.Colors.YELLOW, f"Delete existing file in drive: {file['title']} (Folder: {parent_folder_name} - {parent_folder_id})")
        file.Trash()
    # Upload
    file_upload = gg_drive.CreateFile({"title": file_name, "parents": [{"kind": "drive#fileLink", "id": parent_folder_id}]})
    file_upload.SetContentFile(src)
    file_upload.Upload()
    utils.ColorPrint(utils.Colors.GREEN, f"Uploaded {src} to drive")
    return file_name, str(file_upload['alternateLink']).replace("usp=drivesdk", "usp=share_link")

############################################################################################

def main():
    input_parser = argparse.ArgumentParser(description="Upload builds to google drive")
    input_parser.add_argument('-s', dest='src', help='source path')
    input_parser.add_argument('-d', dest="dest", help='destination path')

    args = input_parser.parse_args()

    if os.path.exists(args.src):
        gg_drive = fun_connect_gg_drive()
        file_name, share_link = fun_upload_to_drive(gg_drive, args.src, args.dest)
        utils.ColorPrint(utils.Colors.GREEN, f"[ShareLink] {file_name}: {share_link}")
    else:
        utils.ColorPrint(utils.Colors.RED, f"File not found: {args.src}")

############################################################################################

if __name__ == '__main__':
    main()

############################################################################################