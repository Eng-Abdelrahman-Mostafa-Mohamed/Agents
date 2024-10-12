from llama_index.core.tools import function_tool
import os


note_path='./note.txt'
def save_note(note):
    if os.path.exists(note_path):
        with open('note.txt', 'w') as f:
            f.write(note)
    else:
        with open('note.txt', 'a') as f:
            f.write(note)
    return 'Note saved successfully'

note_engine = function_tool.FunctionTool.from_defaults(fn=save_note
                                                       ,name='save_note',
                                                       description='Save note to file',
                                                    #    inputs=['note'],
                                                    )
