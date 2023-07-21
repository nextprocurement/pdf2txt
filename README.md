# NextProcurement Project (v2)

Pipeline (version 2) for NextProcurement Project.


## About the tool
It labels each pdf section according its function in the document (Title, header, paragraph...)

## Usage

### Environment Setup


Check requirements.txt to see all requiered packages.

A virtual environment ready-to-use has been created for the CTE-AMD cluster. All dependencies has been installed.
To start it up:


```bash
cd /gpfs/projects/bsc88/projects/NextProcurement_v2
source use_env_venv.sh
```
### Usage

```bash
python model_trainer/pipeline/pipeline.py  \
        --input <pdf file> | <folder with pdf files>> \
        --output <output folder> \
        --model <model paht> (desired model classify the sections (excluding tables) (title, header,etc.) )
```

#### Example of use

```bash
python pipeline/pipeline.py  \
        --input /gpfs/projects/bsc88/projects/NextProcurement_v2/TESTING/INPUT/folder_with_pdfs \
        --output testing_docs/OUTPUT \
        --model /gpfs/projects/bsc88/projects/NextProcurement/model_trainer/output/NextProcurement/next_procurement_v0_8_0.00005_date_22-08-13_time_04-51-37 \
```
#### Ouput format

*output* will be a folder containing a subfolder for each document in *input*. Each subfolder will contain:
- **Doc_labeled_sections.txt** : A plain .txt:  with a label above each paragraph
- **page_X.jpg** : Several .jpg files for each page in the document. Each image has colored rectangle over each paragraph and its corresponding label. An example looks like this:

![alt text](https://github.com/TeMU-BSC/NextProcurement_v2/blob/main/img/page_0.jpg "Example of an page_X.jpg")




