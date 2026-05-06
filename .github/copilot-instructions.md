# Context Resolution Policy

## PROJECT_NAME = define the project name here

1. When a request is made, the system will first analyze the local PROJECT_NAME context folder for relevant information before accessing the global PROJECT_NAME context folder.
2. For each request, first analyze folders and subfolders in the context sources before producing an answer.
3. Local PROJECT_NAME context folder: /context
4. Global PROJECT_NAME context folder(Documentos/General/Proyectos/PROJECT_NAME) : https://grupologisticoandreani.sharepoint.com/:f:/t/AutomatizacinQA/IgA37HWX3DLLSYc-4AcICD5-Ab0sWK1Ur33cFttfBBgjUTg?e=6nn2aw
5. If local and global context conflict, prioritize local context unless the user explicitly requests otherwise.
6. If you find reusable information that helps solve requests, save a concise note in memory for future use.