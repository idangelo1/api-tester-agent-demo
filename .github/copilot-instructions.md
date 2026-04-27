## Context Resolution Policy
PROJECT_NAME = define the project name here
- When a request is made, the system will first analyze the local PROJECT_NAME context folder for relevant information before accessing the global PROJECT_NAME context folder.
- For each request, first analyze folders and subfolders in the context sources before producing an answer.
- Local PROJECT_NAME context folder: /context
- Global PROJECT_NAME context folder(Documentos/General/Proyectos/PROJECT_NAME) : https://grupologisticoandreani.sharepoint.com/:f:/t/AutomatizacinQA/IgA37HWX3DLLSYc-4AcICD5-Ab0sWK1Ur33cFttfBBgjUTg?e=6nn2aw
- If local and global context conflict, prioritize local context unless the user explicitly requests otherwise.
- If you find reusable information that helps solve requests, save a concise note in memory for future use.