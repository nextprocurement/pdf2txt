from pdf_to_text import *
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import argparse
import sys
import os
import logging
import shutil


def process_doc(pdf_path, pipe,output_path):
    '''Processes and saves each pdf file'''

    # Create folder for output
    docname = os.path.basename(os.fsdecode(pdf_path)).split('.')[0]
    processed_output_folder= os.path.join(output_path,docname + '_processed')

    if  os.path.exists(processed_output_folder):
        logging.warning('Directory: ' + str(processed_output_folder) + ' already exits. Overwriting it!')
        shutil.rmtree(processed_output_folder)           # Removes all the subdirectories!
    os.makedirs(processed_output_folder)


    image_and_paragraphs = get_paragraphs_from_pdf(pdf_path)

    with open(os.path.join(processed_output_folder, 'Doc_labeled_sections.txt'), 'w') as f:

        for page, (image, paragraphs) in enumerate(image_and_paragraphs):
            paragraphs_coords_and_labels = []
            f.write('## PAGE:'+ str(page) + ' ##\n\n')
            for text, coords, img in paragraphs:
                is_table = detect_table(img)
                if not is_table: #Process if not table
                    label = pipe(text)
                    f.write('#' + str(label[0]['label']).upper().strip() + ':\n' + text.rstrip() + '\n')
                else:
                    label = "Table"
                    f.write('#' + label.upper() + ':\n' + '...\n')

                paragraphs_coords_and_labels.append([coords, label])


            # img. output
            image_name = f"page_{page}.jpg"
            image_output_path =  os.path.join(processed_output_folder, image_name)
            get_results_visualization(image_output_path, image, paragraphs_coords_and_labels)




def main(*args, **kwargs):


    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]),
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=__doc__)



    parser.add_argument("-i", 
                        "--input",
                        help="PDF doc or directory with several pdf documents")
    
    parser.add_argument("-o", 
                        "--output",
                        help="Output path.")


    parser.add_argument("-m", "--model", 
                        default="../output/NextProcurement/next_procurement_v0_8_0.00005_date_22-08-13_time_04-51-37",
                        help="Path to used doc-processing model.")


    args = parser.parse_args()

     
    # Load model
    tokenizer = AutoTokenizer.from_pretrained(str(args.model))
    model = AutoModelForSequenceClassification.from_pretrained(str(args.model))

    # Load pipeline
    pipe = pipeline("text-classification", model=model, tokenizer=tokenizer)


    if(os.path.isdir(args.input) ):
        for pdf_path in os.listdir(args.input):
            filename = os.fsdecode(pdf_path)
            if filename.endswith(".pdf"): 
                try:
                    process_doc(os.path.join(args.input,pdf_path), pipe, args.output)
                except Exception as e:
                    err_msg = "An error ocurred parsing the document called: " + filename + '. \n\t' + str(e)
                    raise  Exception( err_msg)
            else:
                logging.info('Skipping non-pdf file: ' + filename)
       
    else:#single input doc
        process_doc(args.input, pipe, args.output)





  
    
    


if __name__ == "__main__":
    main()
