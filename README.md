# Upload File To GoogleDrive

Upload file from local to google drive folder and return an internal share link

---
**[Follow Instruction To Get client_serects.json](https://d35mpxyw7m7k7g.cloudfront.net/bigdata_1/Get+Authentication+for+Google+Service+API+.pdf)**
---

## Prepare 
- Replace your client_serects.json was get in previous step
- Edit "ROOT_FOLDER_ID" in upload_ggdrive.py which parent of files will upload

## Run Command
`python upload_ggdrive.py -s "file_path_in_local" -d "path_in_drive"`

## Example
`python upload_ggdrive.py -s "C:/Myfile.txt" -d "Folder1/Folder2/Upload.txt"`