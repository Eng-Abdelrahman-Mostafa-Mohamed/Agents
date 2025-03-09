from llama_index.core.tools import function_tool
import os


note_path='./note.odp'
def save_note(note):
    if os.path.exists(note_path):
        with open('note.odp', 'w') as f:
            f.write(note)
    else:
        with open('note.odp', 'a') as f:
            f.write(note)
    return 'Note saved successfully'

save_note("hello")

note_engine = function_tool.FunctionTool.from_defaults(fn=save_note
                                                       ,name='save_note',
                                                       description='Save note to file',
                                                    #    inputs=['note'],
                                                    )
